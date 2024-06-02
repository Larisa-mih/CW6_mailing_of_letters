from django.core.management import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from newsletter.utils import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_mailing, 'interval', seconds=60)
        scheduler.start()
