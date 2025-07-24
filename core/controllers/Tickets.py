"""Controller to Ticket... Here Create All Logic"""

from django.http.request import HttpRequest, HttpHeaders

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    MyUser,
    Ticket,
    TypeTicket,
    DataTicket,
    Services,
    ServiceTicket,
    ObservationsTicket,
)

from core.serializers import (
    SerializerTicket,
    SerializerDataTicket,
    SerializerObservationsTicket,
    SerializerServices,
    SerializerMyUser,
)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def privateActionsTickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""

    if request.method == "PATCH":
        """Update One"""


@api_view(["GET", "POST"])
def publicActionsTIckets(request: HttpRequest):
    """This a Public Functions to Manage Tickets"""
    if request.method == "GET":
        idTicket = request.query_params.get("ticket")

        if not idTicket:
            return Response(
                {"Message": "Ticket ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            ticket = Ticket.objects.get(pk=idTicket)
        except Ticket.DoesNotExist:
            return Response(
                {"Message": " Ticket not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = DataTicket.objects.filter(Ticket=ticket)
        observations = ObservationsTicket.objects.filter(ticket=ticket)

        user = ticket.user

        serviceTicket = ServiceTicket.objects.filter(ticket=ticket).first()
        serializerService = {"data": None}

        if serviceTicket:
            try:
                service = Services.objects.get(pk=serviceTicket.service.pk)
                serializerService = SerializerServices(service).data
            except Services.DoesNotExist:

                print(
                    f"Warning: Service related to ServiceTicket {serviceTicket.pk} not found."
                )

        # * Serializer Data
        ticketSerializer = SerializerTicket(ticket)
        userSerializer = SerializerMyUser(user)
        dataSerializer = SerializerDataTicket(data, many=True)
        observationsSerializer = SerializerObservationsTicket(observations, many=True)

        send = {
            "ticket": ticketSerializer.data,
            "user": userSerializer.data,
            "data": dataSerializer.data,
            "observations": observationsSerializer.data,
            "service": serializerService.data,
        }

        return Response(send, status=status.HTTP_200_OK)

    if request.method == "POST":
        ticketData = request.data.get("ticket")
        typeTicketName = request.data.get("typeTicket")
        email = request.data.get("user")

        if not all([ticketData, typeTicketName, email]):
            return Response(
                {"message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            typeTicket = TypeTicket.objects.get(name=typeTicketName)
            user = MyUser.objects.get(email=email)
            ticket = Ticket(typeTicket=typeTicket, user=user)
            ticket.save()

            if isinstance(ticketData, dict):
                for key, value in ticketData.items():
                    # TODO: In this loop Need get a Service
                    if key == "service":
                        service = Services.objects.get(name=ticketData["service"])
                        serviceTicket = ServiceTicket(service=service, ticket=ticket)
                        serviceTicket.save()
                    else:
                        addQuotationsMarks = lambda value: (
                            str(value) if isinstance(value, list) else f'"{value}"'
                        )
                        dataTicket = DataTicket(
                            info=f"{str(key)} : {addQuotationsMarks(value)}",
                            Ticket=ticket,
                        )
                        dataTicket.save()
            send = SerializerTicket(ticket)

            return Response(
                {
                    "id": send.data.get("id"),
                    "code": send.data.get("code"),
                    "createTime": send.data.get("submissionDate"),
                },
                status=status.HTTP_200_OK,
            )

        except TypeTicket.DoesNotExist:
            return Response(
                {"message": f"Ticket type '{typeTicketName}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except MyUser.DoesNotExist:
            return Response(
                {"message": f"User with email '{email}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Services.DoesNotExist:
            return Response(
                {"message": f"Service '{ticketData.get('service')}' not found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            print(f"Error creating ticket: {e}")
            return Response(
                {"error": "An unexpected error occurred while creating the ticket."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
