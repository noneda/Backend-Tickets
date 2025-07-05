from django.db import models
from .TypeTicket import TypeTicket
from .MyUser import MyUser
from django.utils import timezone


class Ticket(models.Model):
    submissionDate = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=9)
    completeDate = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    typeTicket = models.ForeignKey(TypeTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def save(self, **kwargs):
        """This is for make a Code and SubmissionData"""
        date_now = timezone.now().date()

        prefix = "XX"
        if self.typeTicket.name == "Mesa de Ayuda":
            prefix = "MA"
        elif self.typeTicket.name == "Pagina Web":
            prefix = "PW"
        elif self.typeTicket.name == "Correos y Usuarios":
            prefix = "CU"

        today_tickets = Ticket.objects.filter(
            submissionDate__date=date_now, code__startswith=prefix
        ).order_by("-code")

        if today_tickets.exists():
            last_code = today_tickets.first().code
            last_number = int(last_code[2:])
            new_number = last_number + 1
        else:
            new_number = 1
        code = f"{prefix}{new_number:03d}"

        self.code = code
        super().save(**kwargs)

    def Mark(self):
        self.active = False
        self.completeDate = timezone.now()
        self.save()
