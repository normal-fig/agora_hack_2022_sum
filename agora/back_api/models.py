from django.db import models


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

