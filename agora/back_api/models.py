from django.db import models
from django.conf import settings


class ClassificationManager(models.Manager):
  def ref_create(self, refs: dict):
    return self.model(product_id=refs['product_id'], embends=refs['embends'])


class ClassificationModel(models.Model):
  product_id = models.CharField(
    max_length=16,
    unique=True
  )

  embends = models.TextField()

  objects = ClassificationManager()


def check_reference(value):
  try:
    ref = Goods.objects.get(product_id=value)
    return ref.is_reference
  except:
    return False


class ReferenceManager(models.Manager):
  def ref_create(self, **kwargs):
    return self.model(**kwargs)


class Reference(models.Model):
  product_id = models.CharField(
    max_length=16,
    primary_key=True
  )
  name = models.TextField()
  props = models.TextField()

  objects = ReferenceManager()



class Goods(models.Model):
  product_id = models.CharField(
    max_length=16,
    primary_key=True
  )
  name = models.TextField()
  props = models.TextField()
  is_reference = models.BooleanField()
  reference_id = models.ForeignKey(
    'Goods',
    on_delete=models.DO_NOTHING,
    null=True,
  )