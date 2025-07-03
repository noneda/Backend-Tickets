from core.models import Services, Secretariat
from core.serializers import SerializerServices, SerializerSecretariat

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def getBasics(request: HttpRequest):
    """Get All Services"""
    try:
        allServices = Services.objects.all()
        allSecretariat = Secretariat.objects.all()
        sendServices = SerializerServices(allServices, many=True)
        sendSecretariat = SerializerSecretariat(allSecretariat, many=True)

        send = {"services": sendServices.data, "secretariats": sendSecretariat.data}
        return Response(send, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
