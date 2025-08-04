from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from core.models import Ticket
from core.serializers import SerializerTicket


@receiver(post_save, sender=Ticket)
def ticketCreatedHandler(sender, instance, created, **kwargs):
    """
    Signal handler that fires after a Ticket object is  saved
    """
    channel_layer = get_channel_layer()

    serializer = SerializerTicket(instance)
    ticket_data = serializer.data

    async_to_sync(channel_layer.group_send)(
        "tickets_updates",
        {
            "type": "ticket_updated_message",
            "message": ticket_data,
            "is_new": created,
        },
    )
    action = "creado" if created else "actualizado"
    print(
        f"Signal: Ticket {instance.id} ({action}) enviado al grupo 'tickets_updates' (created={created})."
    )
