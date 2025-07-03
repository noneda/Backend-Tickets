from django.db import models
from .TypeTicket import TypeTicket
from .MyUser import MyUser
from django.utils import timezone


class Ticket(models.Model):
    submissionDate = models.DateTimeField(default=timezone.now)
    code = models.CharField(max_length=20)
    completeDate = models.DateTimeField()
    active = models.BooleanField(default=True)
    typeTicket = models.ForeignKey(TypeTicket, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    

    def save(self, *args, **kwargs):
        """This is for make a Code and SubmissionData"""
        date_now = timezone.now().date()

        prefix = "XX"
        if self.typeTicket_id == 0:
            prefix = "MA"
        elif self.typeTicket_id == 1:
            prefix = "PW"
        elif self.typeTicket_id == 2:
            prefix = "CU"

        today_tickets = Ticket.objects.filter(
            submissionDate=date_now, code__startswith=prefix
        ).order_by("-code")

        if today_tickets.exists():
            last_code = today_tickets.first().code
            last_number = int(last_code[2:])
            new_number = last_number + 1
        else:
            new_number = 1

        self.code = f"{prefix}{new_number:03d}"

        super().save(*args, **kwargs)

    def Mark(self):
        self.active = False
        self.completeDate = timezone.now()
        self.save()
