from django.urls import path

from .views import (
    add_roles, add_user, delete_roles, delete_user, detail_user, login_user, logout_user, roles_list, search,
    update_roles, update_user, user_list
)

urlpatterns = [

    path("", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("user/", add_user, name="user"),
    path("user_list/", user_list, name="user_list"),
    path("role_list/", roles_list, name="role_list"),
    path("update_user/<str:pk>/", update_user, name="update_user"),
    path("detail_user/<str:pk>/", detail_user, name="detail_user"),
    path("delete_user/<str:pk>/", delete_user, name="delete_user"),
    path("roles/", add_roles, name="roles"),
    path("update_roles/<str:pk>/", update_roles, name="update_roles"),
    path("delete_roles/<str:pk>/", delete_roles, name="delete_roles"),
    path("search/", search, name="search"),

]
