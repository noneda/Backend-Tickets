from django.db import models


class TypeTicket(models.Model):
    """Model from TypeTicket"""

    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name
