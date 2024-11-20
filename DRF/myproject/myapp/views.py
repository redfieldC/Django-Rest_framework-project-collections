from django.shortcuts import render
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination
from .throttles import CustomUserThrottle
from rest_framework.exceptions import NotFound,ValidationError

# Create your views here.

# Viewset
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset=Item.objects.all()
#     serializer_class=ItemSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([CustomUserThrottle])
def allItems(request):
    items = Item.objects.all().order_by('id')
    paginator = CustomPagination()
    paginated_items = paginator.paginate_queryset(items,request)
    serializer = ItemSerializer(paginated_items,many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createItem(request):
    # serializer = ItemSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data,status=status.HTTP_201_CREATED)
    # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    serializer = ItemSerializer(data=request.data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    serializer.save()
    return Response(serializer.data,status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateItem(request,item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({'detail':f'Item with id: {item_id} not found'},status=status.HTTP_404_NOT_FOUND)

    serializer = ItemSerializer(item,data=request.data,partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getItem(request,item_id):
    # try:
    #     item=Item.objects.get(id=item_id)
    # except Item.DoesNotExist:
    #     return Response({'detail':f'Item with id: {item_id} not found'},status=status.HTTP_404_NOT_FOUND)
    
    # serializer = ItemSerializer(item)
    # return Response(serializer.data,status=status.HTTP_200_OK)
    item = Item.objects.filter(id=item_id).first()
    if not item:
        raise NotFound(detail='Item not found')  # Automatically returns a 404 response
    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteItem(request,item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        raise NotFound(detail=f'Item with id {item_id} not found')  # Raises a 404 error

    deletedItem = ItemSerializer(item).data  
    item.delete()
    return Response({
        'detail': f'Item with id {deletedItem["id"]} deleted successfully',
        'deleted_item': deletedItem
    }, status=status.HTTP_200_OK)