from django.contrib import admin
from .models import *

models = [DataTicket, Documents, MyUser, Secretariat, Services, Ticket, TypeTicket]

for model in models:
    admin.site.register(model)
