from datetime import datetime
import json
import math

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import Ticket, TypeTicket
from core.serializers import SerializerTicket


# !IMPORTANT To account for serialization and DRF models, we wrap it in Database_sync_to_async to make them asynchronous... This gave me many inconveniences...
class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Handles new WebSocket connections.
                Authenticates the user and accepts the connection if the user is not anonymous.
        """
        print(f"Intentando conectar usuario: {self.scope['user']}")
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close(code=403)
            return
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnections.
            Currently, it does nothing specific on disconnect.
        """
        print(f"Desconectado con código: {close_code}")
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
            group = int(1 + data.get("group", 0))
            group_size = 20

            filters = {}
            dataFilterApplied = False

            if "active" in data:
                filters["active"] = data["active"]

            if "typeTicket" in data and data["typeTicket"]:
                type_ticket_name = data["typeTicket"]
                filters["typeTicket__name__icontains"] = type_ticket_name

            if "code" in data and data["code"]:
                filters["code__icontains"] = data["code"]

            if "date" in data and data["date"]:
                try:
                    parsed_date = datetime.strptime(data["date"], "%Y/%m/%d").date()
                    filters["submissionDate__date"] = parsed_date
                    dataFilterApplied = True
                except ValueError:
                    await self.send_json(
                        {"error": "Fecha inválida. Usa el formato YY/MM/DD"}
                    )
                    return

            print(filters)

            tickets_qs = await self.get_filtered_queryset(filters)
            total = await self.count_queryset(tickets_qs)

            if dataFilterApplied and total == 0:
                print(
                    "No results found with date filter. Fetching all tickets instead."
                )
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
            print(all_groups)
            await self.send_json({"allGroups": all_groups, "tickets": serialized_data})

        except json.JSONDecodeError:
            await self.send_json({"error": "Formato Json invalido."})

        except Exception as e:
            await self.send_json({"error": f"Error interno: {str(e)}"})

    async def send_json(self, data):
        """
        Helper method to send JSON data over the WebSocket.
        """
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_filtered_queryset(self, filters):
        """
        Asynchronously fetches a filtered queryset of Ticket objects from the database.
        """
        return (
            Ticket.objects.only("id", "submissionDate", "code", "active", "typeTicket")
            .filter(**filters)
            .order_by("-submissionDate")
        )

    @database_sync_to_async
    def get_all_tickets(self):
        """
        Asynchronously fetches all Ticket objects from the database.
        Used as a fallback when a date filter yields no results.
        """
        return Ticket.objects.only(
            "id", "submissionDate", "code", "active", "typeTicket"
        ).order_by("-submissionDate")

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
