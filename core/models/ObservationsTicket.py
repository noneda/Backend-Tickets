from django.db import models
from .Ticket import Ticket


class ObservationsTicket(models.Model):
    """Model from Observation Tickets"""

    text = models.TextField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
