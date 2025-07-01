from django.core.management.base import BaseCommand
from core.models import TypeTicket
from django.db import IntegrityError

services_cota = [
    "Mesa de Ayuda",
    "Pagina Web",
    "Correos y Usuarios",
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Command for Insert All Services..."""

        self.stdout.write("Insert Services...")

        if TypeTicket.objects.exists():
            self.stdout.write(
                self.style.ERROR("The App get All Data... There's no need")
            )

        else:
            for name in services_cota:
                try:
                    typeTicket = TypeTicket.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f"Inserted: {name}"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Already exists: {name}"))

        show = TypeTicket.objects.all()
        self.stdout.write(self.style.SUCCESS(f"\nTotal Services: {show.count()}"))
