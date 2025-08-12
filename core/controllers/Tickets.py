"""Controller to Ticket... Here Create All Logic"""

from datetime import datetime


from django.http.request import HttpRequest, HttpHeaders
from django.db import transaction

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import (
    MyUser,
    Ticket,
    DataTicket,
    Services,
    ServiceTicket,
    ObservationsTicket,
    TypeTicket,
)

from core.serializers import (
    SerializerTicket,
    SerializerObservationsTicket,
    SerializerServices,
    SerializerMyUser,
)

import json, ast


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def privateActionsTickets(request: HttpRequest):
    """This a Private Functions to Manage Tickets"""
    if request.method == "PATCH":
        idTicket = request.data.get("ticket")
        observations = request.data.get("observation")
        state = request.data.get("state")
        print(observations)

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
        with transaction.atomic():
            if isinstance(observations, list):
                existing_observations_texts = set(
                    obs.text for obs in ObservationsTicket.objects.filter(ticket=ticket)
                )

                for value in observations:
                    if isinstance(value, str):
                        cleaned_value = value.strip()
                        if cleaned_value:
                            if cleaned_value not in existing_observations_texts:
                                try:
                                    ticketObservation = ObservationsTicket(
                                        text=cleaned_value, ticket=ticket
                                    )
                                    ticketObservation.save()
                                    existing_observations_texts.add(cleaned_value)
                                except Exception as e:
                                    print(
                                        f"Error saving observation for ticket {idTicket}: {e}"
                                    )
                                    raise

            if isinstance(state, str) and state.strip():
                new_state = state.strip()
                if new_state != ticket.state:
                    ticket.state = new_state

            ticket.Mark()
            ticket.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(["GET", "POST"])
def publicActionsTickets(request: HttpRequest):
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
            if not (submissionDate and code):
                return Response(
                    {"Message": "Ticket ID or submissionDate and Code is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                try:
                    parsedDate = datetime.strptime(submissionDate, "%Y/%m/%d").date()
                    ticket = Ticket.objects.get(
                        code=code, submissionDate__date=parsedDate
                    )

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

        dataItems = DataTicket.objects.filter(Ticket=ticket)
        dataDict = []

        for item in dataItems:
            infoStr = item.info

            try:
                parts = infoStr.split(" : ", 1)
                key = parts[0].strip()
                value = parts[1].strip()

                parsedValue = value

                try:
                    parsedValue = json.loads(value)
                except json.JSONDecodeError:
                    try:
                        parsedValue = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        parsedValue = value

                dataDict.append({key: parsedValue})

            except Exception as e:
                print(f"Error parsing DataTicket ID {item.id}: '{infoStr}' - {e}")

        observations = ObservationsTicket.objects.filter(ticket=ticket)

        user = ticket.user

        serviceTicket = ServiceTicket.objects.filter(ticket=ticket).first()
        serializerService = None

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
            "service": serializerService,
        }

        return Response(send, status=status.HTTP_200_OK)

    if request.method == "POST":
        ticketData = request.data.get("ticket")
        typeTicketName = request.data.get("typeTicket")
        user = request.data.get("user")

        print(ticketData, typeTicketName, user)
        if not all([ticketData, typeTicketName, user]):
            return Response(
                {"message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        """Create Ticket"""
        try:
            user = MyUser.objects.get(email=user)
            typeTicket = TypeTicket.objects.get(name=typeTicketName)
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
