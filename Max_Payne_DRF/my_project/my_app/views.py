from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404
# Create your views here.

class ParentsList(APIView):
    def get(self,request,parent_id=None):
        if parent_id is None:
            parents=Parent.objects.all()
            all_parents_serializer=ParentSerializer(parents,many=True)
            return Response(all_parents_serializer.data,status=status.HTTP_200_OK)
        else:
            parent=Parent.objects.get(id=parent_id)
            parent_serializer=ParentSerializer(parent)
            return Response(parent_serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        create_parent_serializer=ParentSerializer(data=request.data)
        if create_parent_serializer.is_valid():
            create_parent_serializer.save()
            return Response(create_parent_serializer.data,status=status.HTTP_201_CREATED)
        return Response(create_parent_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,parent_id):
        parent=Parent.objects.get(id=parent_id)
        update_parent_serializer=ParentSerializer(parent,data=request.data,partial=True)
        if update_parent_serializer.is_valid():
            update_parent_serializer.save()
            return Response(update_parent_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(update_parent_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class ChildrenList(APIView):
    def get(self,request,children_id=None):
        if children_id is None:
            childrens=Children.objects.all()
            all_childrens_serializer=ChildrenSerializer(childrens,many=True)
            return Response(all_childrens_serializer.data,status=status.HTTP_200_OK)
        else:
            children=Children.objects.get(id=children_id)
            children_serializer=ChildrenSerializer(children)
            return Response(children_serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        create_parent_serializer=ChildrenSerializer(data=request.data)
        if create_parent_serializer.is_valid():
            create_parent_serializer.save()
            return Response(create_parent_serializer.data,status=status.HTTP_201_CREATED)
        return Response(create_parent_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,children_id):
        children = get_object_or_404(Children, id=children_id)
        update_children_serializer=ChildrenSerializer(children,data=request.data,partial=True)
        if update_children_serializer.is_valid():
            update_children_serializer.save()
            return Response(update_children_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(update_children_serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        



class CalculateSum(APIView):
    def post(self,request):
        calc_serializer=CalculateSumSerializer(data=request.data)
        if calc_serializer.is_valid():
            num1=calc_serializer.validated_data["num1"]
            num2=calc_serializer.validated_data["num2"]
            _sum=num1+num2 

            return Response({"sum":_sum},status=status.HTTP_201_CREATED)
        return Response(calc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
