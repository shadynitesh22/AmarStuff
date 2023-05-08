from users.forms import RolesForm, UserEditForm, UserForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import redirect, render

from core.decorators import admin_only

from .models import Customer, Roles


@admin_only
def user_list(request):
    user = Customer.objects.all().order_by("id")
    roles = Roles.objects.all().order_by("id")
    user_count = user.count()
    roles_count = roles.count()

    context = {"user": user, "user_count": user_count, "roles_count": roles_count, "roles": roles_count}
    return render(request, "users/user_list.html", context)


@admin_only
def roles_list(request):
    user = Customer.objects.all().order_by("id")
    roles = Roles.objects.all()
    user_count = user.count()
    roles_count = roles.count()

    context = {"user": user, "user_count": user_count, "roles_count": roles_count, "roles": roles}
    return render(request, "users/roles_list.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Username password incorrect")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have signed  out" + request.user.username)
    return redirect("login")


@admin_only
def add_user(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():

            form.save()
            messages.success(request, "Account has been successfully created")
            return redirect("user_list")
        else:
            messages.error(request, "error")

    context = {"form": form}
    return render(request, "users/Adduser.html", context)


@admin_only
def add_roles(request):
    form = RolesForm()
    if request.method == "POST":
        form = RolesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Role has been created ")
            return redirect("role_list")

    context = {"form": form}
    return render(request, "users/AddRoles.html", context)


def update_user(request, pk):
    user = Customer.objects.get(id=pk)
    form = UserEditForm(instance=user)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated !!")
            return redirect("user_list")

    context = {"form": form}
    return render(request, "users/UpdateUser.html", context)


def detail_user(request, pk):
    user = Customer.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form, "user": user}
    return render(request, "users/DetailUser.html", context)


@admin_only
def delete_user(request, pk):
    user = Customer.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User Deleted")
        return redirect("user_list")

    context = {"item": user}
    return render(request, "system/confirm_delete_user.html", context)


@admin_only
def update_roles(request, pk):
    roles = Roles.objects.get(id=pk)
    form = RolesForm(instance=roles)
    if request.method == "POST":
        form = RolesForm(request.POST, instance=roles)
        if form.is_valid():

            form.save()
            messages.success(request, "Roles have been updated")

            return redirect("role_list")

    context = {"form": form}
    return render(request, "users/updateRoles.html", context)


@admin_only
def delete_roles(request, pk):
    roles = Roles.objects.get(id=pk)
    if request.method == "POST":
        roles.delete()
        messages.success(request, "Roles has been deleted")
        return redirect("role_list")

    context = {"item": roles}
    return render(request, "system/confirm_delete_roles.html", context)


def search(request):
    results = []
    if request.method == "GET":
        query = request.GET.get("search")
        if query == "":
            query = "None"
        results = Customer.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query))
    return render(request, "users/user_results.html", {"query": query, "results": results})
