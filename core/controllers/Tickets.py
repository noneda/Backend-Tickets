"""Controller to Ticket... Here Create All Logic"""

from datetime import datetime


from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

import math
import datetime

from core.models import (
    MyUser,
    Ticket,
    TypeTicket,
    DataTicket,
    Services,
    ServiceTicket,
)

from core.serializers import SerializerTicket


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def privateTicketsGetWebhook(request: HttpRequest):
    """Get all tickets paginated, with optional filters"""
    try:
        group = int(request.query_params.get("grupo", 1))
        groupSize = 20

        getAllTickets = Ticket.objects.only(
            "id", "submissionDate", "code", "active", "typeTicket"
        ).order_by("-submissionDate")

        date_str = request.query_params.get("submissionDate")
        if date_str:
            try:
                parsed_date = datetime.datetime.strptime(date_str, "%y/%m/%d").date()
                getAllTickets = getAllTickets.filter(submissionDate__date=parsed_date)
            except ValueError:
                return Response(
                    {"error": "Fecha inválida. Usa el formato aa/mm/dd"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        total = getAllTickets.count()
        allGroups = math.ceil(total / groupSize)

        start = (group - 1) * groupSize
        end = start + groupSize
        ticketsGroup = getAllTickets[start:end]

        serializerTicket = SerializerTicket(ticketsGroup, many=True)
        send = {
            "allGroups": allGroups,
            "tickets": serializerTicket.data,
        }

        return Response(send, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def privateActionsTickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""

    if request.method == "PATCH":
        """Update One"""


@api_view(["GET", "POST"])
def publicActionsTIckets(request: HttpRequest):
    """This a Public Functions to Manage Tickets"""
    if request.method == "GET":
        return Response({"Message": "TicketOnlyOne..."})

    if request.method == "POST":
        ticketData = request.data.get("ticket")
        typeTicketName = request.data.get("typeTicket")
        email = request.data.get("user")
        try:
            typeTicket = TypeTicket.objects.get(name=typeTicketName)
            user = MyUser.objects.get(email=email)
            ticket = Ticket(typeTicket=typeTicket, user=user)
            ticket.save()

            if isinstance(ticketData, dict):
                for key, value in ticketData.items():
                    # TODO: In this loop Need get a Service
                    if key == "service":
                        service = Services.objects.get(name=ticketData["service"])
                        serviceTicket = ServiceTicket(service=service, ticket=ticket)
                        serviceTicket.save()
                    else:
                        addQuotationsMarks = lambda value: (
                            str(value) if isinstance(value, list) else f'"{value}"'
                        )
                        dataTicket = DataTicket(
                            info=f"{str(key)} : {addQuotationsMarks(value)}",
                            Ticket=ticket,
                        )
                        dataTicket.save()
            send = SerializerTicket(ticket)

            # TODO: Extra... this convert submissionDate to a format more simple
            date = send.data.get("submissionDate")
            format = datetime.fromisoformat(date.replace("Z", "+00:00"))
            submission = format.strftime("%Y-%m-%d")
            return Response(
                {
                    "id": send.data.get("id"),
                    "code": send.data.get("code"),
                    "createTime": submission,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
