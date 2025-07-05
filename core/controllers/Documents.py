from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Ticket, Documents, Secretariat


@api_view(["POST"])
def publicSendDocuments(request: HttpRequest):
    secretariatName = request.data.get("secretariat")
    documentsData = request.FILES.getlist("documents")
    idTicket = request.data.get("ticket")
    try:
        secretariat = Secretariat.objects.only("id").get(name=secretariatName)
        ticket = Ticket.objects.only("id").get(pk=idTicket)

        if not documentsData:
            return Response(
                {"error": "No se recibieron archivos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for archivo in documentsData:
            Documents.objects.create(
                name=archivo.name,
                content=archivo,
                secretariat=secretariat,
                ticket=ticket,
            )

        return Response({"message": "GetData"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": f"Internal server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
