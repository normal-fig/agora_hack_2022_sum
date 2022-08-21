from django.contrib import admin
from back_api.models import Reference


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
  pass