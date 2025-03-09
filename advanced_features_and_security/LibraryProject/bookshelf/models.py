from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.

class CustomUserManager(BaseUserManager):
  """Manager for custom user model"""

  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError(_("Users must have an email address"))
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    "create and return a superuser"
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    return self.create_user(email, password, **extra_fields)
  
class CustomUser(AbstractUser):
  username = None
  email = models.EmailField(unique=True)
  date_of_birth = models.DateField(null=Trueu, blank=True)
  profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

  USERAME_FIELD = "email"
  REQUIRED_FIELDS = ["first_name", "last_name"]

  objects = CustomUserManager()

  def __str__(self):
    return self.email
  
class SomeModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Book(models.Model):
  title = models.CharField(max_length=200)
  author = models.CharField(max_length=100)
  publication_year = models.IntegerField()


  def __str__(self):
    return self.title

class Article(models.Model):
    """Example model with custom permissions."""
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_view", "Can view articles"),
            ("can_create", "Can create articles"),
            ("can_edit", "Can edit articles"),
            ("can_delete", "Can delete articles"),
        ]

    def __str__(self):
        return self.title