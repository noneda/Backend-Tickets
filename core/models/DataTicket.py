from django.db import models
from .Ticket import Ticket


class DataTicket(models.Model):

    info = models.TextField()
    Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
