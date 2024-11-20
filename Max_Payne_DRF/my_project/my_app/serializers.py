from rest_framework import serializers
from .models import *
class ParentSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(max_length=30)
    last_name=serializers.CharField(max_length=30)
    age=serializers.IntegerField(default=1)
    
    def create(self,validated_data):
        return Parent.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance
    
    def validate_age(self,age):
        if age < 18:
            raise serializers.ValidationError(f"Age of parent must be 18 or older")
        return age 
        

class ChildrenSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(max_length=30)
    last_name=serializers.CharField(max_length=30)
    age=serializers.IntegerField(default=1)
    created_at=serializers.DateTimeField(read_only=True)
    parent=serializers.PrimaryKeyRelatedField(queryset=Parent.objects.all())

    def create(self,validated_data):
        parent=validated_data.pop("parent",None)
        if parent is None:
            raise serializers.ValidationError("Parent for the child is mandatory")
        child=Children.objects.create(parent=parent,**validated_data)
        return child 

    def update(self,instance,validated_data):
        parent=validated_data.pop("parent",None)
        if parent:
            try:
                instance.parent = parent
            except Parent.DoesNotExist:
                raise serializers.ValidationError({"parent": f"Parent {parent.id} does not exist."})
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        

        instance.save()
        return instance 

class CalculateSumSerializer(serializers.Serializer):
    num1=serializers.IntegerField()
    num2=serializers.IntegerField()
    _sum=serializers.IntegerField(read_only=True)

    def validate_num1(self, value):
        if value is None:
            raise serializers.ValidationError("num1 cannot be empty")
        if value <= 0:
            raise serializers.ValidationError("num1 must be a positive number")
        return value
    
    