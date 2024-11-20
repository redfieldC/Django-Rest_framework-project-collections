from django.urls import path,include
from . import views
urlpatterns = [
    path("all-person/",views.all_persons),
    path("create-person/",views.create_person),
    path("delete-person/<int:id>/",views.delete_person),
    path("update-person/<int:id>/",views.update_person)
]
