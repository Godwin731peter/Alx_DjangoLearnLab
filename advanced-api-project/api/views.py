from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from serializers import BookSerializer
from django_filters import rest_fraework
from .models import Book

# Create your views here.
class BookListView(generics.ListAPIView):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderigFilter]
  search_fields = ['title', 'author_name']
  filterset_fields = ['title', 'author_name', 'publication_year']
  ordering_fields = ['title', 'author_name', 'publication_year',]

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