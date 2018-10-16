from django.conf import settings
from django.core.management.base import CommandError, BaseCommand

from project.airtable import AirtableSynchronizer, Airtable


class Command(BaseCommand):
    help = 'Synchronize with Airtable.'

    def handle(self, *args, **options):
        if not settings.AIRTABLE_API_KEY:
            raise CommandError("AIRTABLE_API_KEY must be configured.")

        self.stdout.write("Retrieving current Airtable...\n")
        syncer = AirtableSynchronizer(Airtable(max_retries=99))
        syncer.sync_users(stdout=self.stdout)

        self.stdout.write("Finished synchronizing with Airtable!\n")
