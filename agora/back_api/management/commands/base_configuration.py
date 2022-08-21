from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
  help = "startup command"

  def handle(self, *args, **options):
    
    if not User.objects.filter(username='admin').exists():
      User.objects.create_superuser('admin', 'admin@jam.as', 'admin')
      self.stdout.write(self.style.SUCCESS(f'adding default superuser'))

    try:
      from back_api.nnmodel import get_recmodel
      from back_api.serializers import ProductsSerializer
      import json
      model = get_recmodel()

      with open(settings.MEDIA_ROOT / 'init.json', 'r') as inp:
        data = json.load(inp)

      ser = ProductsSerializer(data=data, many=True)
      if ser.is_valid():
        refs_qs = ser.validated_data
        model.update_embends(refs_qs)
    except:
      pass