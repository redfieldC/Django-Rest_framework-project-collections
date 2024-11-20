from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import authenticate
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
# Create your views here.
class AllUsers(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            all_users = CustomUser.objects.all()  # Query to get all users
            all_users_serializers = CustomUserSerializer(all_users, many=True)  # Serialize the users
            return Response(all_users_serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Catch any exception that might occur
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CreateUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        create_user_serializer = CustomUserSerializer(data=request.data)
        if create_user_serializer.is_valid():
            create_user_serializer.save()
            return Response(create_user_serializer.data, status=status.HTTP_201_CREATED)

        return Response(create_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UpdateUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def patch(self,request,id):
        user=CustomUser.objects.get(id=id)
        update_user_serializer=CustomUserSerializer(user,data=request.data,partial=True)
        if update_user_serializer.is_valid():
            update_user_serializer.save()
            return Response(update_user_serializer.data,status=status.HTTP_202_ACCEPTED)
        username=update_user_serializer.data["username"]
        update_user_serializer.validate_username(username)
        return Response(update_user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginUser(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")

        if not username or not password:
            return Response({"error":"Username and password are required"},status=status.HTTP_400_BAD_REQUEST)

        user=authenticate(username=username,password=password)
        if not user:
            return Response({"error":"Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)
        
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            "token":token.key,
            "message":"Login successfull"
            },
            status=status.HTTP_202_ACCEPTED
        )
    

class LogoutUser(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def post(self,request):
        try:
            request.user.auth_token.delete()
            return Response({
                "message":"Logout successful"
                },
                status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {
                    "error":f"An error occured {str(e)}"
                }
                ,
                status=status.HTTP_401_UNAUTHORIZED
            )
        

class CreateTodo(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data 
        data["user"]=request.user.id
        create_task_serializer=TaskSerializer(data=data)
        if create_task_serializer.is_valid():
            create_task_serializer.save()
            return Response({"data":create_task_serializer.data},status=status.HTTP_201_CREATED)
        return Response({"error":create_task_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveAllOrRetreiveOneOrUpdateOrDeleteTodo(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def patch(self,request,id):
        todo=Task.objects.get(id=id)
        update_todo_serializer=TaskSerializer(todo,data=request.data,partial=True)
        if update_todo_serializer.is_valid():
            update_todo_serializer.save()
            return Response({"data":update_todo_serializer.data,"message":"Todo updated successfully"})
        return Response({"message":"Todo not updated","error":update_todo_serializer.errors})
    
    def get(self,request,id=None):
        if id is None:
            todo=Task.objects.filter(user=request.user)
            all_todo_serializer=TaskSerializer(todo,many=True)
            return Response({"data":all_todo_serializer.data},status=status.HTTP_200_OK)
        else:
            todo=Task.objects.filter(user=request.user).first()
            todo_serializer=TaskSerializer(todo)
            return Response({"data":todo_serializer.data},status=status.HTTP_200_OK)

