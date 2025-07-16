from django.contrib.auth import authenticate
from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def doTokenWhenLoginUser(request: HttpRequest):
    """Login user and return authentication token."""

    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = authenticate(username=username, password=password)

        if user:
            if user.is_staff:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "No tienes permisos de Administrador."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response(
                {"message": "Datos Incorrectos."}, status=status.HTTP_401_UNAUTHORIZED
            )

    except Exception as e:
        return Response(
            {"message": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def confirmationToken(request: HttpRequest):
    """Confirms if a token is valid and returns user info"""
    return Response({"status": True}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def deleteTokenWhenLogOutUser(request: HttpRequest):
    """Logout: Deletes the token of the authenticated user"""

    try:
        request.user.auth_token.delete()
        return Response(
            {"message": "Token deleted successfully. Logged out."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response(
            {"message": f"Token could not be deleted: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
