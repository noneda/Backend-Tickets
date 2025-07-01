from django.core.management.base import BaseCommand
from core.models import Secretariat
from django.db import IntegrityError


secretariats_cota = [
    "Despacho del Alcalde",
    "Secretaría de Planeación",
    "Secretaría General y Gobierno",
    "Secretaría de Salud",
    "Secretaría de Infraestructura y Obras Públicas",
    "Secretaría de Hacienda",
    "Secretaría de Educación",
    "Secretaría de Desarrollo Social",
    "Secretaría de Cultura y Juventudes",
    "Secretaría de Talento Humano",
    "Secretaría de Control Interno",
    "SAMADE",
    "IMRD",
    "Cedro Mall",
    "Casa Social de la mujer",
    "Secretaría de Tránsito, Transporte y Movilidad",
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Command for Insert All Secretariats..."""

        self.stdout.write("Insert Secretariats...")

        if Secretariat.objects.exists():
            self.stdout.write(
                self.style.ERROR("The App get All Data... There's no need")
            )

        else:
            for name in secretariats_cota:
                try:
                    secretariat = Secretariat.objects.create(name=name)
                    self.stdout.write(self.style.SUCCESS(f"Inserted: {name}"))
                except IntegrityError:
                    self.stdout.write(self.style.ERROR(f"Already exists: {name}"))

        show = Secretariat.objects.all()
        self.stdout.write(self.style.SUCCESS(f"\nTotal secretariats: {show.count()}"))
