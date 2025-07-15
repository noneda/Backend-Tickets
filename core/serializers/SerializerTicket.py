from ..models.Ticket import Ticket
from rest_framework import serializers


class SerializerTicket(serializers.ModelSerializer):
    typeTicket = serializers.CharField(source="typeTicket.name")

    class Meta:
        model = Ticket
        fields = "__all__"
