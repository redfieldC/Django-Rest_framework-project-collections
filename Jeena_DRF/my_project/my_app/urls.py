from django.urls import path,include
from .views import *
urlpatterns = [
    path('authors/<int:author_id>/',AuthorsView.as_view()),
    path('authors/',AuthorsView.as_view()),
    path("books/",BooksView.as_view()),
    path("books/<int:book_id>/",BooksView.as_view())
]
