from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates a Moderators group'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Moderators')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Moderators group'))
        else:
            self.stdout.write(self.style.WARNING('Moderators group already exists'))
