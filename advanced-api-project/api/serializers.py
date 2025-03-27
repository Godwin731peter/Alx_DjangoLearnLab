from rest_framework import serializers
from rest_framework import permissions
from .models import Book, Author
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.

    Validation:
        - Ensures the publication year is not in the future.
    """

    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensures books cannot be assigned a publication year in the future.
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
class IsAdminOrReadOnly(permissions.BasePermission):
    # Read only for everyyone write permission for admin
    def has_perission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff       


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.

    Relationship Handling:
        - Includes nested serialization of books written by the author.
    """

    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ['name', 'books']
