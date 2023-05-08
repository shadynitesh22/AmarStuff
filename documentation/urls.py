from django.urls import path

from .views import delete_form, detail_documents, documentation_start, form_update, list_documents, shippers_form

urlpatterns = [

    path("documentation-form/<str:pk>/", documentation_start, name="documentation-form"),

    path("documentation-list/", list_documents, name="list-documentation"),
    path("documentation-detail/<str:pk>/", detail_documents, name="detail-documentation"),
    path("documentation-update/<str:pk>/", form_update, name="update-documentation"),
    path("documentation-delete/<str:pk>/", delete_form, name="delete-documentation"),
    path("documentation-list/", list_documents, name="list-documentation"),
    path("shippers/", shippers_form, name="shippers_form"),

]
