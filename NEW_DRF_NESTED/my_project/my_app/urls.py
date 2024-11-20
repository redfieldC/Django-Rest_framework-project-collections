from django.urls import path,include
from .views import *
urlpatterns = [
    path("all-users/",AllUsers.as_view()),
    path("create-user/",CreateUser.as_view()),
    path("update-user/<int:id>/",UpdateUser.as_view()),
    path("login-user/",LoginUser.as_view()),
    path("logout-user/",LogoutUser.as_view()),
    path("create-todo/",CreateTodo.as_view()),
    path("update-delete-retreive-todo/",RetrieveAllOrRetreiveOneOrUpdateOrDeleteTodo.as_view()),
    path("update-delete-retreive-todo/<int:id>/",RetrieveAllOrRetreiveOneOrUpdateOrDeleteTodo.as_view()),
    # path("create-todo/",CreateTodo.as_view())
]