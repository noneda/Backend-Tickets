from ..models.ServiceTicket import ServiceTicket
from rest_framework import serializers


class SerializerServiceTicket(serializers.ModelSerializer):
    class Meta:
        model = ServiceTicket
        fields = "__all__"
