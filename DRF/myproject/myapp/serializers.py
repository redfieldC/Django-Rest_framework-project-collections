from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework import status

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.save()
    #     return instance

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)  # Make category optional

    class Meta:
        model = Item
        fields = '__all__'

    def update(self, instance, validated_data):
        # Extract and handle the nested category data
        category_data = validated_data.pop('category', None)
        
        # Handle the category update if provided
        if category_data:
            category_instance = instance.category  # Get the related category instance
            if category_instance:
                # Update the category through the CategorySerializer
                category_serializer = CategorySerializer(category_instance, data=category_data, partial=True)
                if category_serializer.is_valid():
                    category_serializer.save()
                else:
                    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'No category assigned to this item'}, status=status.HTTP_400_BAD_REQUEST)

        # Now update other fields in the Item model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


