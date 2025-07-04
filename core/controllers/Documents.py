from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Ticket, Documents, Secretariat


@api_view(["POST"])
def publicSendDocuments(request: HttpRequest):
    secretariatName = request.data.get("secretariat")
    documentsData = request.data.get("documents")
    idTicket = request.data.get("ticket")
    try:
        secretariat = Secretariat.objects.only("id").get(
            name=secretariatName
        )  # * Only need a id
        ticket = Ticket.objects.only("id").get(pk=idTicket)
        

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
