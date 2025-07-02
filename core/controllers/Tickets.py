"""Controller to Ticket... Here Create All Logic"""

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def Tickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""
    if request.method == "GET":
        """This Get All"""

    if request.method == "PATCH":
        """Update One"""


@api_view(["POST"])
def createTIckets(request: HttpRequest):
    """This a Public"""


@api_view(["GET"])
def searchOneTicket(request: HttpRequest):
    """This a Public"""
