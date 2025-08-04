from datetime import datetime
import json
import math

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer


from core.models import Ticket
from core.serializers import SerializerTicket
from rest_framework.authtoken.models import Token


# !IMPORTANT To account for serialization and DRF models, we wrap it in Database_sync_to_async to make them asynchronous... This gave me many inconveniences...
class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handles new WebSocket connections.
                Authenticates the user and accepts the connection if the user is not anonymous.
        """
        print(f"Trying to connect user: {self.scope['user']}")
        user = self.scope["user"]
        self.token_key = self.scope.get("token_key")

        if user.is_anonymous:
            print("Conexión rechazada: Usuario anónimo.")
            await self.close(code=403)
            return

        await self.accept()
        print(f"WebSocket connection accepted for {user.email}.")

        self.group_name = "tickets_updates"
        self.current_filters = {}
        self.current_group = 1

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(f"User {user.email} (ID: {user.id}) add to group '{self.group_name}'.")

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnections.
            Currently, it does nothing specific on disconnect.
        """
        print(f"Disconnected with code: {close_code}")

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(
                f"User {self.scope['user'].email} left the group '{self.group_name}'."
            )

        if self.token_key:
            print(f"Deleting token: {self.token_key}")
            await self.delete_auth_token(self.token_key)
            print(f"Token {self.token_key} removed.")
        else:
            print("There is no token to delete on this connection..")

        pass

    async def receive(self, text_data):
        """
        Receives messages from the WebSocket.
                Parses filters from the incoming JSON, queries tickets, and sends back
                paginated results or an error message.
        """
        try:
            print("Received message, starting processing...")
            data = json.loads(text_data)
            group_size = 20

            self.current_group = int(1 + data.get("group", 0))
            self.current_filters = {}

            dataFilterApplied = False

            if "active" in data:
                self.current_filters["active"] = data["active"]

            if "typeTicket" in data and data["typeTicket"]:
                type_ticket_name = data["typeTicket"]
                self.current_filters["typeTicket__name__icontains"] = type_ticket_name

            if "code" in data and data["code"]:
                self.current_filters["code__icontains"] = data["code"]

            if "date" in data and data["date"]:
                try:
                    parsed_date = datetime.strptime(data["date"], "%Y/%m/%d").date()
                    self.current_filters["submissionDate__date"] = parsed_date
                    dataFilterApplied = True
                except ValueError:
                    await self.send_json(
                        {"error": "Fecha inválida. Usa el formato YY/MM/DD"}
                    )
                    return

            print(
                f"Current customer filters ({self.channel_name}): {self.current_filters}"
            )

            await self._send_current_tickets_to_client(
                self.current_filters,
                self.current_group,
                group_size,
                dataFilterApplied,
            )

        except json.JSONDecodeError:
            await self.send_json({"error": "Formato Json invalido."})

        except Exception as e:
            await self.send_json({"error": f"Error interno: {str(e)}"})

    async def send_json(self, data):
        """
        Helper method to send JSON data over the WebSocket.
        """
        await self.send(text_data=json.dumps(data))

    async def ticket_updated_message(self, event):
        """
        Receive a message from the 'tickets_updates' group when a ticket is created or updated.
        """
        message = event["message"]
        is_new = event.get("is_new", False)
        action_type = "nuevo" if is_new else "actualizado"
        print(
            f"Consumer ({self.channel_name}) received ticket message {action_type}: {message.get('id')}"
        )

        group_size = 20
        await self._send_current_tickets_to_client(
            self.current_filters,
            self.current_group,
            group_size,
            False,
        )
        print(f"Consumer ({self.channel_name}) re-submitted the updated ticket list.")

    async def _send_current_tickets_to_client(
        self, filters, group, group_size, data_filter_applied
    ):
        """
        Helper method to get and send the ticket list to the client.
        """
        tickets_qs = await self.get_filtered_queryset(filters)
        total = await self.count_queryset(tickets_qs)

        if data_filter_applied and total == 0:
            print("No results found with the date filter. Getting all tickets instead.")
            filters_for_all_tickets = {
                k: v
                for k, v in filters.items()
                if not k.startswith("submissionDate__date")
            }
            tickets_qs = await self.get_all_tickets(filters_for_all_tickets)
            total = await self.count_queryset(tickets_qs)

        all_groups = math.ceil(total / group_size)
        start = (group - 1) * group_size
        end = start + group_size
        paginated = await self.slice_queryset(tickets_qs, start, end)

        serialized_data = await self.serialize_tickets(paginated)
        await self.send_json({"allGroups": all_groups, "tickets": serialized_data})

    @database_sync_to_async
    def get_filtered_queryset(self, filters):
        """
        Asynchronously fetches a filtered queryset of Ticket objects from the database.
        """
        return (
            Ticket.objects.only(
                "id",
                "submissionDate",
                "code",
                "active",
                "typeTicket",
                "state",
                "user__email",
            )
            .select_related("typeTicket", "user")
            .filter(**filters)
            .order_by("-submissionDate")
        )

    @database_sync_to_async
    def get_all_tickets(self):
        """
        Asynchronously fetches all Ticket objects from the database.
        Used as a fallback when a date filter yields no results.
        """
        if filters is None:
            filters = {}
        return (
            Ticket.objects.only(
                "id",
                "submissionDate",
                "code",
                "active",
                "typeTicket",
                "state",
                "user__email",
            )
            .select_related("typeTicket", "user")
            .filter(**filters)
            .order_by("-submissionDate")
        )

    @database_sync_to_async
    def count_queryset(self, qs):
        """
        Asynchronously counts the number of items in a given queryset.
        """
        return qs.count()

    @database_sync_to_async
    def slice_queryset(self, qs, start, end):
        """
        Asynchronously slices a queryset to retrieve a specific range of items.
        Converts the slice to a list to ensure database query execution within the sync context.
        """
        return list(qs[start:end])

    @database_sync_to_async
    def serialize_tickets(self, tickets_list):
        """
        Serializes a list of Ticket objects asynchronously.
        """
        serializer = SerializerTicket(tickets_list, many=True)
        return serializer.data

    @database_sync_to_async
    def delete_auth_token(self, token_key):
        """
        Asynchronously removes the authentication token.
        """
        try:
            Token.objects.filter(key=token_key).delete()
            print(f"Token {token_key} removed from the database.")
        except Exception as e:
            print(f"Error al eliminar token {token_key}: {e}")
