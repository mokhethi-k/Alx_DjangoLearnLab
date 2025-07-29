from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer


# BookList is protected by token authentication.
# Only authenticated users can access book data.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = [permissions.IsAuthenticated, permissions.AllowAny]

# BookViewSet is protected by token authentication.
# Only admin users can perform CRUD operations on the book data.
class BookViewSet(viewsets.ModelViewSet):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    
