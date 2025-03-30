from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from serializers import BookSerializer
from .models import Book

# Create your views here.
class BookListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookDetailView(generics.RetrieveAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated]    

class BookUpdateView(generics.UpdateAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permmissionn_classes = [permissions.IsAuthenticated]