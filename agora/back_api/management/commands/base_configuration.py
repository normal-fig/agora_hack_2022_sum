from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
  help = "startup command"

  def handle(self, *args, **options):
    
    if not User.objects.filter(username='admin').exists():
      User.objects.create_superuser('admin', 'admin@jam.as', 'admin')
      self.stdout.write(self.style.SUCCESS(f'adding default superuser'))
