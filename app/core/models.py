"""
Database models.
"""
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
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
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