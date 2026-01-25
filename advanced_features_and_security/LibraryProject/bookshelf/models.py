from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
            
        ]

    def __str__(self):
        return self.title



class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser model.
    Controls how users and superusers are created.
    """

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)





class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.
    """

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username
