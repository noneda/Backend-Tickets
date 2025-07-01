from django.db import models
from .Ticket import Ticket


class DataTicket(models.Model):

    info = models.CharField(max_length=2000)
    Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
