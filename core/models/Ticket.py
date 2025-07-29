from django.db import models, transaction
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

    STATE_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En Progreso"),
        ("resolved", "Resuelto"),
        ("close", "Cerrado"),
        ("cancel", "Cancelado"),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        """
        Custom save method to generate 'code' only upon initial creation
        and ensure atomicity for code generation.
        """
        if not self.pk and not self.code:
            try:
                date_now = timezone.now().date()
                self.state = "pending"
                prefix = "XX"
                if self.typeTicket.name == "Mesa de Ayuda":
                    prefix = "MA"
                elif self.typeTicket.name == "Pagina Web":
                    prefix = "PW"
                elif self.typeTicket.name == "Correos y Usuarios":
                    prefix = "CU"

                with transaction.atomic():
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

                    super().save(*args, **kwargs)
                    return
            except Exception as e:
                print(f"Error create Ticket {e}")
        else:
            super().save(*args, **kwargs)

    def Mark(self, newState=None):
        """
        Marks the ticket as inactive and sets a completion date/time.
            Can also update the state field.
        """
        self.completeDate = timezone.now().date()
        if newState:
            if newState.lower() in [choice[0] for choice in self.STATE_CHOICES]:
                self.state = newState.lower()
                if newState.lower() == ("resoled" or "close" or "cancel"):
                    self.active = False
            else:
                print(
                    f"Invalid state '{newState}' provided to Mark method for ticket {self.pk}"
                )
        self.save()
