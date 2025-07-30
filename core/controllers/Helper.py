from django.http.request import HttpRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import MyUser, Secretariat, Ticket

from core.serializers import SerializerTicket

from core.utils.send_mail import sendBeautifulMail

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
def helperUser(request: HttpRequest):
    """Logic to Create user when don`t Exist"""
    user = request.data.get("user")
    print(user)
    try:
        try:
            user = MyUser.objects.get(email=user.get("email"))
            print("Found...")
        except MyUser.DoesNotExist:
            print("Create...")
            department = user.get("department")
            secretariat = Secretariat.objects.get(name=department)

            fullName = user.get("name", "").strip()
            name = None
            surname = None

            if fullName:
                name_parts = fullName.split(maxsplit=1)
                name = name_parts[0]
            if len(name_parts) > 1:
                surname = name_parts[1]

            createArgs = {
                "email": user.get("email"),
                "name": name,
                "surname": surname,
                "cellphone": user.get("phone", None),
                "secretariat": secretariat,
            }

            user = MyUser.objects.create_user(**createArgs)
            print(f"Successfully created new user: {user.email}")

        return Response(status=status.HTTP_200_OK)
    except Exception:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def helperSendMailWhenCreate(request: HttpRequest):
    """This a helper to send Mail to user"""
    ticket = request.data.get("ticket")
    recipient = request.data.get("mail")
    if not ticket or not recipient or not recipient.get("email"):
        return Response(
            {"detail": "Ticket ID and recipient email are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        try:
            getTicket = Ticket.objects.get(pk=ticket)
            serTicket = SerializerTicket(getTicket).data
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        subject = (
            f"Confirmación de Creación de Ticket - Código: {serTicket.get('code')}"
        )
        email = recipient["email"]
        name = recipient["name"]

        context = {"username": name, "ticket": serTicket}
        sendBeautifulMail(subject, email, context, "createTicket.html")
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def helperSendMailWhenPatch(request: HttpRequest):
    """This a helper to send Mail to user"""
    ticket = request.data.get("ticket")
    recipient = request.data.get("mail")
    if not ticket or not recipient or not recipient.get("email"):
        return Response(
            {"detail": "Ticket ID and recipient email are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        subject = f"Actualización de Ticket - Código: {ticket.get('code')}"
        email = recipient["email"]
        name = recipient["name"]

        context = {"username": name, "ticket": ticket}
        sendBeautifulMail(subject, email, context, "updateTicket.html")
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
