from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None):
        email = self.normalize_email(email),

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name,
            last_name,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    created_at = created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.first_name + ' ' + self.last_name
