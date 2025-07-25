"""
Database Models for User.
"""

from .Secretariat import Secretariat

from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class MyUserManager(BaseUserManager):
    """Manager for User Personalized"""

    def resolve_secretariat(self, secretariat_value):
        if isinstance(secretariat_value, Secretariat):
            return secretariat_value
        elif isinstance(secretariat_value, int):
            return Secretariat.objects.get(id=secretariat_value)
        elif isinstance(secretariat_value, str):
            return Secretariat.objects.get(name=secretariat_value)
        return None

    def create_user(self, email: str, password=None, **extra_fields):
        """Create Save and Return User"""
        if not email:
            raise ValueError(gettext_lazy("The Email must be set"))

        secretariat_value = extra_fields.pop("secretariat", None)
        if secretariat_value:
            try:
                extra_fields["secretariat"] = self.resolve_secretariat(
                    secretariat_value
                )
            except Secretariat.DoesNotExist:
                raise ValueError(f"Secretariat not found: {secretariat_value}")
        else:
            raise ValueError("Secretariat is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    # TODO: This feature is required when creating an administrator model from the user
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    """User Personalized in the System"""

    # * User Data
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    surname = models.CharField(max_length=254)
    cellphone = models.BigIntegerField(null=True, blank=True)

    # * Foreign Key with Secretariat
    secretariat = models.ForeignKey(
        Secretariat, on_delete=models.CASCADE, null=True, blank=True
    )

    # * This User is admin??
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # * Instance Manager
    objects = MyUserManager()

    # * Those is for Config a User
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "cellphone", "secretariat"]
