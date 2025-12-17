from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    help = 'Отправляет рассылку по ID'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки')

    def handle(self, *args, **options):
        mailing = Mailing.objects.get(id=options['mailing_id'])
        send_mailing(mailing)
        self.stdout.write(self.style.SUCCESS(f'Рассылка {mailing.id} отправлена'))


