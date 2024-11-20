from rest_framework import serializers
from .models import *


class PersonSerializers(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    
    name=serializers.CharField(max_length=50)
    description=serializers.CharField(style={"base_template":"textarea.html"},allow_blank=True)
    age=serializers.IntegerField()

    def create(self,validated_data):
        return Person.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance 