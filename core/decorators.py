from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("login")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            roles = None
            user = None
            if request.user.roles:
                roles = request.user.roles.name
            if request.user:
                user = request.user

            if roles in allowed_roles or user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "system/not_allowed.html")

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user:
            group = request.user

        if not group.is_superuser:
            return render(request, "system/not_allowed.html")

        if group.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return None

    return wrapper_function
