from django.db import models
from .Secretariat import Secretariat
from .DataTicket import Ticket
from ..utils.upload_paths import categorized_upload_path


class Documents(models.Model):
    """
    Here Insert All Data from Docs that Insert
    ! This can make a shit...
    """

    name = models.CharField(max_length=254)
    content = models.FileField(upload_to=categorized_upload_path)
    secretariat = models.ForeignKey(Secretariat, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
