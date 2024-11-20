from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
# Create your views here.

@api_view(['GET'])
def all_persons(request):
    persons = Person.objects.all()
    serializer = PersonSerializers(persons,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
def create_person(request):
    serializers = PersonSerializers(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_409_CONFLICT)

@api_view(['PATCH'])
def update_person(request,id):
    person=Person.objects.get(id=id)
    serializers=PersonSerializers(person,data=request.data,partial=True)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status=status.HTTP_202_ACCEPTED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_person(request,id):
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist:
        return Response({"message":"Person does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    person.delete()
    return Response({"message":"Person deleted successfully"},status=status.HTTP_200_OK)
        