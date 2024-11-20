from django.urls import path,include
from .views import *
urlpatterns = [
    
    path("parents/",ParentsList.as_view()),
    path("parents/<int:parent_id>/",ParentsList.as_view()),
    path("children/",ChildrenList.as_view()),
    path("children/<int:children_id>/",ChildrenList.as_view()),
    path("calc_sum/",CalculateSum.as_view())

]