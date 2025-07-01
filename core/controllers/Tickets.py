"""Controller to Ticket... Here Create All Logic"""

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET", "POTS", "PATCH"])
def Tickets(request: HttpRequest):
    if request.method == "GET":
        """"""
    if request.method == "POST":
        """Create a Ticket"""
        
    if request.method == "PATCH":
        """"""
