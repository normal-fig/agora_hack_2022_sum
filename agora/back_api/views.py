from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from back_api.serializers import ProductsSerializer, MatchProductsSerializer
from back_api.nnmodel import get_recmodel


@api_view(['POST'])
def match_products(request: Request):
  ser = ProductsSerializer(data=request.data, many=True)
  if ser.is_valid(True):
    goods_qs = ser.validated_data
    model = get_recmodel()
    preds = model.predict(goods_qs)

    ret_data = model.ser.mp_concat(goods_qs, preds, model.model.ids)
    mp_ser = MatchProductsSerializer(data=ret_data, many=True)
    mp_ser.is_valid(True)

    return Response(data=mp_ser.validated_data,status=status.HTTP_200_OK)
  return Response(data=ser.validated_data,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_refs(request: Request):
  ser = ProductsSerializer(data=request.data, many=True)
  if ser.is_valid():
    refs_qs = ser.validated_data
    model = get_recmodel()
    try: 
      model.update_embends(refs_qs)
    except:
      return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status=status.HTTP_202_ACCEPTED)
  return Response(data=ser.validated_data,status=status.HTTP_400_BAD_REQUEST)
