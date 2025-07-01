from django.db import models


class Services(models.Model):
    """Model for Services"""

    name = models.CharField(max_length=255, unique=True)
