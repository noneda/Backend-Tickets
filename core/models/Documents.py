from django.db import models
from .Secretariat import Secretariat
from .DataTicket import DataTicket
from ..utils.upload_paths import categorized_upload_path


class Documents(models.Model):
    """
    Here Insert All Data from Docs that Insert
    ! This can make a shit...
    """

    name = models.CharField(max_length=254)
    content = models.FileField(upload_to=categorized_upload_path)
    secretariat = models.ForeignKey(Secretariat, on_delete=models.CASCADE)
    dataTicket = models.ForeignKey(DataTicket, on_delete=models.CASCADE)
