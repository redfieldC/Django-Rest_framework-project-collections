from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api-auth-token/',obtain_auth_token),
    path('all-items/',views.allItems),
    path('create-item/',views.createItem),
    path('get-item/<int:item_id>/',views.getItem),
    path('update-item/<int:item_id>/',views.updateItem),
    path('delete-item/<int:item_id>/',views.deleteItem)

]