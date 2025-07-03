from django.db import models
from .Ticket import Ticket
from .Services import Services


class ServiceTicket(models.Model):
    """Model from ServicesTicket"""

    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
