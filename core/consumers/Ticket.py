from datetime import datetime
import json
import math

from channels.generic.websocket import AsyncWebsocketConsumer

from core.models import Ticket
from core.serializers import SerializerTicket
from channels.db import database_sync_to_async


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            await self.close(code=403)
            return
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            user = self.scope["user"]
            if user.is_anonymous:
                await self.send_json({"error": "No autenticado"})
                return

            data = json.loads(text_data)
            group = int(data.get("group", 1))
            group_size = 20

            filters = {}

            if "active" in data:
                filters["active"] = data["active"]

            if "typeTicket" in data and data["typeTicket"]:
                filters["typeTicket__icontains"] = data["typeTicket"]

            if "code" in data and data["code"]:
                filters["code__icontains"] = data["code"]

            if "date" in data and data["date"]:
                try:
                    parsed_date = datetime.strptime(data["date"], "%y/%m/%d").date()
                    filters["submissionDate__date"] = parsed_date
                except ValueError:
                    await self.send_json(
                        {"error": "Fecha inválida. Usa el formato aa/mm/dd"}
                    )
                    return

            tickets_qs = await self.get_filtered_queryset(filters)

            total = await self.count_queryset(tickets_qs)
            all_groups = math.ceil(total / group_size)
            start = (group - 1) * group_size
            end = start + group_size
            paginated = await self.slice_queryset(tickets_qs, start, end)

            serializer = SerializerTicket(paginated, many=True)
            await self.send_json({"allGroups": all_groups, "tickets": serializer.data})

        except Exception as e:
            await self.send_json({"error": f"Error interno: {str(e)}"})

    async def send_json(self, data):
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_filtered_queryset(self, filters):
        return (
            Ticket.objects.only("id", "submissionDate", "code", "active", "typeTicket")
            .filter(**filters)
            .order_by("-submissionDate")
        )

    @database_sync_to_async
    def count_queryset(self, qs):
        return qs.count()

    @database_sync_to_async
    def slice_queryset(self, qs, start, end):
        return list(qs[start:end])


# * HTTP get Tickets... (Just in case)
# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def privateTicketsGetWebhook(request: HttpRequest):
#     """Get all tickets paginated, with optional filters"""
#     try:
#         group = int(request.query_params.get("group", 1))
#         groupSize = 20

#         getAllTickets = Ticket.objects.only(
#             "id", "submissionDate", "code", "active", "typeTicket"
#         ).order_by("-submissionDate")

#         date_str = request.query_params.get("date")
#         if date_str:
#             try:
#                 parsed_date = datetime.datetime.strptime(date_str, "%y/%m/%d").date()
#                 getAllTickets = getAllTickets.filter(submissionDate__date=parsed_date)
#             except ValueError:
#                 return Response(
#                     {"error": "Fecha inválida. Usa el formato aa/mm/dd"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         total = getAllTickets.count()
#         allGroups = math.ceil(total / groupSize)

#         start = (group - 1) * groupSize
#         end = start + groupSize
#         ticketsGroup = getAllTickets[start:end]

#         serializerTicket = SerializerTicket(ticketsGroup, many=True)
#         send = {
#             "allGroups": allGroups,
#             "tickets": serializerTicket.data,
#         }

#         return Response(send, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response(
#             {"error": f"Internal server error: {str(e)}"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )
