from django.contrib import admin
from back_api.models import Goods, ClassificationModel, Reference


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
  pass

@admin.register(ClassificationModel)
class ClassificationModelAdmin(admin.ModelAdmin):
  pass

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
  pass