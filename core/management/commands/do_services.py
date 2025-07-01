from django.core.management.base import BaseCommand
from core.models import Services
from django.db import IntegrityError

services_cota = [
    "Activación de Internet",
    "Falla de Internet",
    "Configuración Impresora",
    "Falla de Computador",
    "Telefonía Fija",
    "Configuración Correo",
    "Desactivación y activación de correo electrónico",
    "Instalación de Software",
    "Configuración de Equipo Cómputo Nuevo",
    "Solicitud de proceso COPIAS DE SEGURIDAD Y/O BACKUP'S",
    "Carpetas Compartidas",
    "Capacitación",
    "Proyectos y adquisición de Tecnología",
    "Cambio de Tóner/Recipient residual de tóner",
    "Otros",
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Command for Insert All Services..."""

        self.stdout.write("Insert Services...")

        if Services.objects.exists():
            self.stdout.write(
                self.style.ERROR("The App get All Data... There's no need")
            )

        else:
            for name in services_cota:
                try:
                    service = Services.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f"Inserted: {name}"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Already exists: {name}"))

        show = Services.objects.all()
        self.stdout.write(self.style.SUCCESS(f"\nTotal Services: {show.count()}"))
