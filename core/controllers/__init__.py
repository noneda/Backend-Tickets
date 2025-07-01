from django.http.request import HttpRequest, HttpHeaders


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def info(request: HttpRequest):
    """This is a root path from App"""
    return Response(
        data={
            "name": "Alcaldía Area de las TIC Manejo de Tickets y Solicitudes",
            "Author": "noneda",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def verifyTokenSuccessful(request: HttpRequest):
    """Test to Verify that token Work"""
    return Response(
        data={
            "Successful": "You're authenticated",
            "Author": "noneda",
        },
        status=status.HTTP_200_OK,
    )
