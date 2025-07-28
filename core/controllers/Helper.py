from django.http.request import HttpRequest
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import MyUser, Secretariat

from core.serializers import SerializerMyUser

from core.utils.send_mail import (
    createTicketMessage,
    simpleSendMail,
    sendBeautifulMail,
)


@api_view(["GET"])
def helperUser(request: HttpRequest):
    """Logic to Create user when don`t Exist"""
    user = request.query_params.get("user")
    try:
        user = MyUser.objects.get(email=user.get("email"))
    except MyUser.DoesNotExist:
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

    send = SerializerMyUser(user).data

    return Response({"user", send["id"]}, status=status.HTTP_200_OK)


api_view(["POST"])


def helperSendMail(request: HttpRequest):
    """This a helper to send Mail to user"""
    ticket = request.data.get("ticket")
    recipient = request.data.get("mail")
    try:

        subject = f"Confirmación de Creación de Ticket - Código: {ticket.get('code')}"
        email = recipient["email"]
        name = recipient["name"]

        # * Simple Email
        # message = createTicketMessage(user.name, infoTicket)
        # simpleSendMail(subject, message, recipientEmail)

        # * Email with Steroids
        context = {"username": name, "ticket": ticket}
        sendBeautifulMail(subject, email, context)
        return Response(
            {"message": "Successful Mail Send"}, status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            {
                "message": "Error to send a Mail",
                "error": f"Internal server error: {str(e)}",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
