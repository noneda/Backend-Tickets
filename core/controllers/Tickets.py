"""Controller to Ticket... Here Create All Logic"""

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Ticket, TypeTicket, Services, MyUser


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def privateActionsTickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""
    if request.method == "GET":
        """This Get All"""

    if request.method == "PATCH":
        """Update One"""


@api_view(["GET", "POST"])
def publicActionsTIckets(request: HttpRequest):
    """This a Public Functions to Manage Tickets"""
    if request.method == "GET":
        return Response({"Message": "TicketOnlyOne..."})

    if request.method == "POST":
        ticketData = request.data.get("ticket")
        print(ticketData)
        return Response({"message": "DataGet"}, status=status.HTTP_200_OK)
