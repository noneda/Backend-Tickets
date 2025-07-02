from core.models import Services
from core.serializers import SerializerServices

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def getServices(request: HttpRequest):
    """Get All Services"""
    try:
        all = Services.objects.all()
        send = SerializerServices(all, many=True)  
        return Response(
            send.data, status=status.HTTP_200_OK
        )  

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
