from django.db import models


class Secretariat(models.Model):
    """Model For Secretary"""
    
    name = models.CharField(max_length=254, unique=True)
