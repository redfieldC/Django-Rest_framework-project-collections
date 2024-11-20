from rest_framework import serializers
from .models import *
from django.db import IntegrityError

class CustomUserSerializer(serializers.ModelSerializer):
    username_email=serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = "__all__"


    def get_username_email(self,instance):
            return instance.username + " " + instance.email 


    def create(self, validated_data):
        try:
            username = validated_data.get('username')
            email = validated_data.get('email')
            mobile_number = validated_data.get('mobile_number')
            password = validated_data.get('password')

            if not username:
                raise serializers.ValidationError("Username cannot be empty.")
            if not email:
                raise serializers.ValidationError("Email cannot be empty.")
            if not mobile_number:
                raise serializers.ValidationError("Mobile number cannot be empty.")
            if not password:
                raise serializers.ValidationError("Password cannot be empty.")



            user = CustomUser(
                username=username,
                email=email,
                mobile_number=mobile_number
            )
            user.set_password(password)  
            user.save() 

            return user
        
        except Exception as e:
            raise serializers.ValidationError(f"Unexpected error occurred: {str(e)}")

    def update(self,instance,validated_data):
        for attr,value in validated_data.items():
            if attr=="password":
                instance.set_password(value)
            else:
                setattr(instance,attr,value)
        instance.save()
        return instance
    
    def validate_username(self, value):
        print("I am at the validate_username!!!!")
        if self.instance:  # If instance exists, we're updating, so check against other users
            if CustomUser.objects.filter(username=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(f"This username '{value}' is already taken. Please try another.")
        else:  # We're creating a new user
            if CustomUser.objects.filter(username=value).exists():
                raise serializers.ValidationError(f"This username '{value}' is already taken. Please try another.")
        return value 

    def validate_email(self, value):
        if self.instance:  # If instance exists, we're updating, so check against other users
            if CustomUser.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(f"This email '{value}' is already taken. Please try another.")
        else:  # We're creating a new user
            if CustomUser.objects.filter(email=value).exists():
                raise serializers.ValidationError(f"This email '{value}' is already taken. Please try another.")
        return value 

    def validate_mobile_number(self, value):
        if self.instance:  
            if CustomUser.objects.filter(mobile_number=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(f"This mobile number '{value}' is already taken. Please try another.")
        else:  
            if CustomUser.objects.filter(mobile_number=value).exists():
                raise serializers.ValidationError(f"This mobile number '{value}' is already taken. Please try another.")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep = {"username":rep.get("username"),"email":rep.get("email"),"mobile_number":rep.get("mobile_number"),"username_email": rep.get("username_email")}
        return rep 

def validated_title_length(value):
    if len(value) < 3:
        raise serializers.ValidationError("The length of the title MUST be at least 3 or more characters!!!!!")



class TaskSerializer(serializers.ModelSerializer):
    title=serializers.CharField(validators=[validated_title_length])
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'is_completed', 'created_at', 'updated_at','user']
        read_only_fields = ['created_at', 'updated_at']  

    

    def create(self, validated_data):
        user = validated_data.pop('user')  
        task = Task.objects.create(user=user,**validated_data)  
        return task

    def update(self, instance, validated_data):
        user = validated_data.get('user', instance.user)
        
        if user != instance.user:
            raise serializers.ValidationError("You can only update your own tasks.")
        
      
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()
        return instance

    def validate_title(self,value):
        if not value:
            raise serializers.ValidationError({"error":f"title cannot be empty"})
        return value 
    
    def validate_description(self,value):
        if not value:
            raise serializers.ValidationError({"error":f"description cannot be empty"})
        return value 
    
    def validate_is_completed(self,value):
        if value not in [True,False]:
            raise serializers.ValidationError(f"is_completed can only have value of either True or False")
        return value 
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return instance 
