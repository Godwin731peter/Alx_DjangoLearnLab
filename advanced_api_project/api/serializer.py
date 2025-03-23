from .models import Book, Author
from rest_framework import serializers
from datetime import date

# 
class BookSerializer(serializers.ModelSerializer):
  # converts book instances to JSON format 
  # includes all fields from the book model
  #implements custom validation to ensure publication year is accurate 
  class meta:
      model = Book
      fields = ['title', 'publication_year', 'author']

  def validate_publication_year(self, value): 
    # validate to check the publication year
    if value < datetime.today():
      raise serializers.ValidationError("publication date cannot be in the future")
    return value

class AuthorSerializer(serializers.ModelSerializer):
  #converts Author instances to JSON format
  #includes the 'name' field from the Author model
  #using nested serialization to dynamicall include books written by the author
  #the book field is a nested serializer that ensures multiple books can be serialized and also prevents book from beign created
  books = BookSerializer(many=True, read_only=True)
  class meta:
      model = name
      fields = ['name','books']