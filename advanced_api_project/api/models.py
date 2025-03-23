from django.db import models

# Create your models here.
# this creates a model name in your database with a string field
class Author(models.Model):
  name = models.StringField(max_length=250)

# This create title, pub_year, and author foreignkey to your database
class Book(models.Model):
  title = models.StringField()
  publication_year = IntegerField()
  author = models.ForeignKey(Author, on_delete=models.Cascade)