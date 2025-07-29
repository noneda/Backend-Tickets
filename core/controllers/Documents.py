from django.http.request import HttpRequest, HttpHeaders
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Ticket, Documents, Secretariat
from core.serializers import SerializerDocuments


@api_view(["GET", "POST"])
def publicDocuments(request: HttpRequest):
    if request.method == "GET":
        """Get method to a ticket Documents by ticket id"""
        id = request.query_params.get("ticket")

        if not id:
            return Response(
                {"message": "Ticket ID is required for get a Documents"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            ticket = get_object_or_404(Ticket, pk=id)
            documents = Documents.objects.filter(ticket=ticket)
            serializer = SerializerDocuments(
                documents, many=True, context={"request": request}
            ).data
            return Response({"documents": serializer}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket don`t found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Error with server to get a Documents: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    if request.method == "POST":
        """Post method to send a ticket documents"""
        secretariatName = request.data.get("secretariat")
        documentsData = request.FILES.getlist("documents")
        idTicket = request.data.get("ticket")
        print(secretariatName, documentsData, idTicket)

        if not idTicket:
            return Response({"error": "Ticket requerido"}, status=400)

        try:
            secretariat = Secretariat.objects.only("id").get(name=secretariatName)
            ticket = Ticket.objects.only("id").get(pk=idTicket)

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
