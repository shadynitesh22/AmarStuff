from urllib import request

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission, PermissionsMixin
from django.db import models

# Create your models here.


class UserManger(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):
        if username is None:
            raise TypeError("User must have a username")

        if email is None:
            raise TypeError("User must have a email")
        if password is None:
            raise TypeError("User must have a password")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):

        if password is None:
            raise TypeError("")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Roles(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    permissions = models.ManyToManyField(
        Permission,
        verbose_name="permissions",
        blank=True,
    )

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, null=True, blank=True, unique=True)
    email = models.EmailField(max_length=100, null=False, blank=False)
    roles = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManger()

    def __str__(self):
        return self.username


class UserActivity(models.Model):
    deleted = models.DateTimeField(auto_now_add=True, db_index=True, editable=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(
        Customer,
        null=True,
        db_index=True,
        on_delete=models.DO_NOTHING,
        editable=False,
    )

    NON_CUSTOM_DB_FIELDS = ("created_by", "updated_by")

    def save(self, *args, **kwargs):
        if not hasattr(self, "_user"):
            user = request.user
            if not user:
                user = request.user
        else:
            user = self._user
        if user and user.is_authenticated:
            self.update_by = user
            if "update_fields" in kwargs and "updated_by" not in kwargs["update_fields"]:
                kwargs["update_fields"].append("update_by")

        if not self.pk:
            self.created_by = user
            if "update_fields" in kwargs and "created_by" not in kwargs["update_fields"]:
                kwargs["update_field"].append("created_by")
        super(UserActivity, self).save(*args, **kwargs)

    class Meta:
        abstract = True
