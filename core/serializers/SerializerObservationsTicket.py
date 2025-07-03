from ..models.ObservationsTicket import ObservationsTicket
from rest_framework import serializers


class SerializerObservationsTicket(serializers.ModelSerializer):
    class Meta:
        model = ObservationsTicket
        fields = "__all__"
