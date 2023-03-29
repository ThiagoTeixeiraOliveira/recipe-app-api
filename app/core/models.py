"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class UserManager(BaseUserManager):
    """Manager for users."""

    # extra_fields can provide keyword arguments, giving flexibility
    # as it means we dont need to update create_user method
    # because it automatically provides them when we call the method
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


"""
AbstractBaseUser -> Contains the functionality for the authentication
                    system(but not any fields)
PermissionsMixin -> Contains the functionality for the permissions feature
                    of Django and contains fields that are needed for this
                    permissions feature
"""
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Defines the field used for authentication
    # (how we replace default field "username")
    USERNAME_FIELD = 'email'

"""
In this case, as we are just creating a simple vanilla model
to store the recipes, we are baseing after models.Model,
the base model class provided by Django.
For the user, we were extending the existing functionality of the
user
"""
class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    """
    With Text field, we can hold more content and more lines
    in comparison to Char Field.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
