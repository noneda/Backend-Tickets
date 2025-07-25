from ..models.MyUser import MyUser
from rest_framework import serializers


class SerializerMyUser(serializers.ModelSerializer):
    """Serializer for User... don`t send a password..."""

    secretariat = serializers.CharField(source="secretariat.name")

    class Meta:
        model = MyUser
        fields = ["id", "email", "secretariat", "name", "surname", "cellphone"]
