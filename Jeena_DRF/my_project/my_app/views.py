from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.
class AuthorsView(APIView):
    def get(self,request,author_id=None):
        if author_id is not None:
            try:
                author=Authors.objects.get(id=author_id)
            except Exception as e:
                return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
            author_serializer=AuthorsSerializer(author)
            return Response(author_serializer.data,status=status.HTTP_200_OK)
        else:
            all_authors=Authors.objects.all()
            all_authors_serializer=AuthorsSerializer(all_authors,many=True)
            return Response(all_authors_serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        create_author_serializer=AuthorsSerializer(data=request.data)
        if create_author_serializer.is_valid():
            create_author_serializer.save()
            return Response(create_author_serializer.data,status=status.HTTP_201_CREATED)
        return Response(create_author_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,author_id):
        try:
            author=Authors.objects.get(id=author_id)
        except Exception as e:
            return Response({"error":str(e)})
        update_author_serializer=AuthorsSerializer(author,data=request.data,partial=True)
        if update_author_serializer.is_valid():
            update_author_serializer.save()
            return Response(update_author_serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(update_author_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class BooksView(APIView):
    def get(self, request, book_id=None):
        if book_id:
            book = Books.objects.get(id=book_id)
            serializer = BooksSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            # return Response(BooksSerializer(book).data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, book_id):
        book = Books.objects.get(id=book_id)
        serializer = BooksSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            updated_book = serializer.save()
            # return Response(BooksSerializer(updated_book).data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
