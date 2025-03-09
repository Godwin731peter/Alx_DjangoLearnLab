from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Article
from .models import CustomUser
from .models import Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'publication_year')
  search_fields = ('title', 'author')
  list_filter = ('publication_year',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "date_of_birth", "profile_photo", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser, CustomUserAdmin)


content_type = ContentType.objects.get_for_model(Article)

# Create groups
viewers = Group.objects.get_or_create(name="Viewers")[0]
editors = Group.objects.get_or_create(name="Editors")[0]
admins = Group.objects.get_or_create(name="Admins")[0]

# Get permissions
can_view = Permission.objects.get(codename="can_view", content_type=content_type)
can_create = Permission.objects.get(codename="can_create", content_type=content_type)
can_edit = Permission.objects.get(codename="can_edit", content_type=content_type)
can_delete = Permission.objects.get(codename="can_delete", content_type=content_type)

# Assign permissions
viewers.permissions.add(can_view)
editors.permissions.add(can_view, can_create, can_edit)
admins.permissions.add(can_view, can_create, can_edit, can_delete)