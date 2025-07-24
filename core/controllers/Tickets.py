"""Controller to Ticket... Here Create All Logic"""

from datetime import datetime, date


from django.http.request import HttpRequest, HttpHeaders
from django.db import transaction

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
    SerializerObservationsTicket,
    SerializerServices,
    SerializerMyUser,
)

import json


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def privateActionsTickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""
    if request.method == "PATCH":
        idTicket = request.data.get("ticket")
        active = request.data.get("active")
        observations = request.data.get("observation")
        state = request.data.get("state")

        if not idTicket:
            return Response(
                {"Message": " Ticket ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            idTicket = int(idTicket)
        except ValueError:
            return Response(
                {"message": "Invalid ticket ID format. Must be an integer."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            ticket = Ticket.objects.get(pk=idTicket)
        except Ticket.DoesNotExist:
            return Response(
                {"Message": "Ticket not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic:
            if isinstance(observations, list):
                for value in observations:
                    if isinstance(value, str):
                        try:
                            ticketObservation = ObservationsTicket(
                                text=value, ticket=ticket
                            )
                            ticketObservation.save()
                        except Exception as e:
                            print(f"Error saving observation: {e}")
                            raise

            if active is not None and isinstance(active, bool) and active:
                ticket.Mark()

            if isinstance(state, str):
                ticket.state = state

            return Response(status=status.HTTP_202_ACCEPTED)


@api_view(["GET", "POST"])
def publicActionsTIckets(request: HttpRequest):
    """This a Public Functions to Manage Tickets"""
    if request.method == "GET":
        idTicket = request.query_params.get("ticket")
        submissionDate = request.query_params.get("submissionDate")
        code = request.query_params.get("code")

        if idTicket:
            try:
                ticket = Ticket.objects.get(pk=idTicket)
            except Ticket.DoesNotExist:
                return Response(
                    {"Message": " Ticket not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            if not submissionDate and code:
                return Response(
                    {"Message": "Ticket ID or submissionDate and Code is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                try:
                    parsedDate = datetime.strptime(submissionDate, "%Y/%m/%d").date()
                    ticket = Ticket.objects.get(code=code, submissionDate=parsedDate)

                except ValueError:
                    return Response(
                        {
                            "Message": "Invalid date format for 'submissionDate'. Please use YYYY/MM/DD."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                except Ticket.DoesNotExist:
                    return Response(
                        {"Message": " Ticket not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        data = DataTicket.objects.filter(Ticket=ticket)
        dataDict = []

        for item in data:
            infoStr = item.info

            try:
                parts = infoStr.split(" : ", 1)
                key = parts[0].strip()
                value = parts[1].strip()

                try:
                    parsed_value = json.loads(value)

                except json.JSONDecodeError:
                    if value.startswith('"') and value.endswith('"'):
                        parsed_value = value[1:-1]
                    else:
                        parsed_value = value

                dataDict.append(parsed_value)

            except Exception as e:
                print(f"Error parsing DataTicket ID {item.id}: '{infoStr}' - {e}")

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
        observationsSerializer = SerializerObservationsTicket(observations, many=True)

        send = {
            "ticket": ticketSerializer.data,
            "user": userSerializer.data,
            "data": dataDict,
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
