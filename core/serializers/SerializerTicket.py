from ..models.Ticket import Ticket
from rest_framework import serializers


class SerializerTicket(serializers.ModelSerializer):
    class Meta:
        model: Ticket
        fields = "__all__"
