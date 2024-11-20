from rest_framework import serializers
from .models import *

class AuthorsSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=50)
    description=serializers.CharField()
    date_of_birth=serializers.DateTimeField(read_only=True)

    def create(self,validated_data):
        validated_data.pop("date_of_birth",None)
        return Authors.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance 
    
class BooksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField()
    authors=serializers.ListField(
        child=serializers.CharField(),write_only=True 
    )

    def create(self, validated_data):
        authors_data = validated_data.pop("authors", [])

        book = Books.objects.create(**validated_data)


        authors_list = []
        for author_name in authors_data:
            try:
                author = Authors.objects.get(name=author_name)
                authors_list.append(author)
            except Authors.DoesNotExist:
                raise serializers.ValidationError(f"Author with name '{author_name}' does not exist.")

        # Set the ManyToMany relationship
        book.authors.set(authors_list)
        return book

    def update(self, instance, validated_data):
        authors_name = validated_data.pop("authors", None)
        if authors_name:
            authors_list = []
            for author_name in authors_name:
                try:
                    author = Authors.objects.get(name=author_name)
                    authors_list.append(author)
                except Exception as e:
                    raise serializers.ValidationError(f"Author with name {author_name} does not exist")

            instance.authors.set(authors_list)  # Replace authors
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        authors = instance.authors.all()
        representation["authors"] = [author.name for author in authors]
        return representation
