"""Controller to Ticket... Here Create All Logic"""

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    MyUser,
    Ticket,
    TypeTicket,
    DataTicket,
    Services,
    ServiceTicket,
)

from core.serializers import SerializerTicket


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
        typeTicketName = request.data.get("typeTicket")
        userId = request.data.get("user")
        try:
            typeTicket = TypeTicket.objects.get(name=typeTicketName)  # * Only need a id
            user = MyUser.objects.get(pk=userId)
            service = None
            if "service" in ticketData:
                service = Services.objects.get(name=ticketData["service"])

            # TODO: DataTicket save logic
            listDataTicket = []
            if isinstance(ticketData, dict):
                for key, value in ticketData.items():
                    # TODO: In this loop Need get a Service
                    if key == "service":
                        break
                    else:
                        addQuotationsMarks = lambda value: (
                            str(value) if isinstance(value, list) else f'"{value}"'
                        )
                        listDataTicket.append(
                            f'"{str(key)}" :  {addQuotationsMarks(value)}'  # ? like a String
                        )
                        # * Here... Is for Save a DataTicket

            # TODO: Here create Ticket...
            # ? Make a Conditionals for see a CODE From tickets it can make a Fixed...
            


            return Response({"message": "GetData"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
