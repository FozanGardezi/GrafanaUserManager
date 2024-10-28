from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class GrafanaOrganization(models.Model):
    name = models.CharField(max_length=255)
    grafaid = models.IntegerField(blank=True, null=True) 

    def __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, login, password, organisation, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, login=login, organisation=organisation, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, login, password, organisation, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(name, email, login, password, organisation, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    grafaid = models.IntegerField(null=True, blank=True, editable=False)
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True, max_length=64)
    login = models.CharField(max_length=32, unique=True)
    organisation = models.ForeignKey(GrafanaOrganization, on_delete=models.CASCADE,  null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "login", "organisation"]

    def __str__(self):
        return self.email