from django.core.management import BaseCommand
from newsletter.utils import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mailing()
