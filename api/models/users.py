from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models

POS_CHOICES = (("SALES", "Sales"), ("SUPPORT", "Support"), ("MANAGEMENT", "Management"))


class UserManager(BaseUserManager):
    def create_superuser(
        self, username, first_name, last_name, email, password, **other_fields
    ):

        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("position", "MANAGEMENT")

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(
            username, first_name, last_name, email, password, **other_fields
        )

    def create_user(
        self, username, first_name, last_name, email, password, **other_fields
    ):
        if not username:
            raise ValueError("You must provide an username")
        if not first_name:
            raise ValueError("You must provide a first name")
        if not last_name:
            raise ValueError("You must provide a last name")
        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    position = models.CharField(choices=POS_CHOICES, default="SUPPORT", max_length=10)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
