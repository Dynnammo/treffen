from django.db.utils import IntegrityError

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = "Create a super admin in the DB. Credentials are in .env"

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(
                os.environ["DJANGO_SUPERUSER_NAME"],
                "",
                os.environ["DJANGO_SUPERUSER_PASSWORD"],
                first_name="Treffen - admin",
            )
            print("Admin account created!")
        except IntegrityError as err:
            print(
                f"Error while creating superuser!"
                f"Maybe it already exists?\nOriginal error: {err}"
            )
