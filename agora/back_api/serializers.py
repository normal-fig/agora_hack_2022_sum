from rest_framework import serializers as ser


def id_validate(value):
  try:
    if value is not None:
      int(value, 16)
    return value
  except:
    raise ser.ValidationError('inccorrect id')



class ProductsSerializer(ser.Serializer):
  id = ser.CharField(
    min_length=0
  )
  
  name = ser.CharField(
    allow_blank=True, 
    allow_null=True
  )

  props = ser.ListField(
    child=ser.CharField(min_length=0, allow_blank=True, 
    allow_null=True),
    allow_null=True
  )



  def validate_id(self, value):
    return id_validate(value)


class MatchProductsSerializer(ser.Serializer):
  id = ser.CharField(
    min_length=0
  )

  reference_id = ser.CharField(
    min_length=0,
    allow_blank=True, allow_null=True
  )

  
  def validate_reference_id(self, value):
    return id_validate(value)

  def validate_id(self, value):
    return id_validate(value)
