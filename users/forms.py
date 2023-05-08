from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Customer, Roles


class UserForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ["username", "email", "roles"]


class UserEditForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ["password", "last_login", "groups", "is_active", "is_staff", "is_superuser", "user_permissions"]


class RolesForm(ModelForm):
    class Meta:
        model = Roles
        fields = "__all__"
