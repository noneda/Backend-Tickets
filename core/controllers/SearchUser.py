from django.http import HttpRequest
from core.models import MyUser, Secretariat
from core.serializers import SerializerMyUser, SerializerSecretariat

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def getUserByEmail(request: HttpRequest):
    """
    Get user and related secretariat info by email passed as query param.
    """
    email = request.query_params.get("email")

    if not email:
        return Response(
            {"error": "Missing 'email' query parameter."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return Response(
            {"error": f"No user found with email: {email}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        secretariat = Secretariat.objects.get(pk=user.secretariat_id)
    except Secretariat.DoesNotExist:
        return Response(
            {"error": f"No secretariat found for user with email: {email}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_data = SerializerMyUser(user).data
    secretariat_data = SerializerSecretariat(secretariat).data

    response_data = {
        "email": user_data.get("email"),
        "name": f"{user_data.get('name', '')} {user_data.get('surname', '')}".strip(),
        "phone": user_data.get("cellphone"),
        "department": secretariat_data.get("name"),
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def suggestUsersByEmail(request: HttpRequest):
    """
    Suggest users by partial email string.
    ?q=partial_email
    """
    query = request.query_params.get("email", "").strip()

    if not query or len(query) < 2:
        return Response(
            {"error": "Please provide at least 2 characters to search."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    emails = list(
        MyUser.objects.filter(email__icontains=query).values_list("email", flat=True)[
            :1
        ]
    )

    if not emails:
        return Response(
            {"message": "No matching emails found."}, status=status.HTTP_404_NOT_FOUND
        )

    return Response({"suggestions": emails[0]}, status=status.HTTP_200_OK)
