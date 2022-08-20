from rest_framework import serializers as ser


def id_validate(value):
  try:
    if value is not None:
      int(value, 16)
    return value
  except:
    raise ser.ValidationError('inccorrect id')


class GoodsSerializer(ser.Serializer):
  product_id = ser.CharField(
    max_length=16,
    min_length=16
  )
  
  name = ser.CharField(
    min_length=0
  )

  props = ser.ListField(
    child=ser.CharField(min_length=0)
  )

  is_reference = ser.BooleanField(

  )

  reference_id = ser.CharField(
    max_length=16,
    min_length=16,
    allow_blank=True, allow_null=True
  )

  def validate_product_id(self, value):
    return id_validate(value)

  def validate_reference_id(self, value):
    return id_validate(value)



class ProductsSerializer(ser.Serializer):
  id = ser.CharField(
    max_length=16,
    min_length=16
  )
  
  name = ser.CharField(
    min_length=0
  )

  props = ser.ListField(
    child=ser.CharField(min_length=0)
  )

  # reference_id = ser.CharField(
  #   min_length=0
  # )



  def validate_id(self, value):
    return id_validate(value)


class MatchProductsSerializer(ser.Serializer):
  id = ser.CharField(
    max_length=16,
    min_length=16
  )

  reference_id = ser.CharField(
    max_length=16,
    min_length=16,
    allow_blank=True, allow_null=True
  )

  
  def validate_reference_id(self, value):
    return id_validate(value)

  def validate_id(self, value):
    return id_validate(value)
