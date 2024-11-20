from rest_framework import serializers
from .models import *



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author','post']

 

class PostSerializer(serializers.ModelSerializer):
    comments  = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'comments']

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])  # Extract nested data
        post = Post.objects.create(**validated_data)

        # Create related comments
        for comment_data in comments_data:
            Comment.objects.create(post=post, **comment_data)

        return post
    
    def update(self, instance, validated_data):
        comments_data = validated_data.pop('comments', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        # Update or create related comments
        for comment_data in comments_data:
            Comment.objects.update_or_create(
                post=instance,
                id=comment_data.get('id'),
                defaults=comment_data
            )

        return instance


