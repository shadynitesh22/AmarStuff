from django.urls import path

from .views import (
    commodity_create, commodity_delete, commodity_list, commodity_update, create_quotation, create_quotation_type,
    create_work_of_scope, dashboard, delete_quotation, delete_quotation_type, delete_work_of_scope, email_page,
    quotation_detail_view, quotation_list, quotation_type_list, receive_email, send_email, update_quotation,
    update_quotation_type, update_work_of_scope, work_of_scope_list
)

urlpatterns = [

    path("dashboard/", dashboard, name="dashboard"),
    path("quotation/", create_quotation, name="quotation-create"),
    path("quotation_list/", quotation_list, name="quotation_list"),
    path("quotation_detail/<str:pk>/", quotation_detail_view, name="quotation_detail"),
    path("update_quotation/<str:pk>/", update_quotation, name="update_quotation"),
    path("delete_quotation/<str:pk>/", delete_quotation, name="delete_quotation"),
    path("quotation_type/", create_quotation_type, name="quotation-create_type"),
    path("quotation_type_list/", quotation_type_list, name="quotation-list_type"),
    path("update_quotation_type/<str:pk>/", update_quotation_type, name="update_quotation_type"),
    path("delete_quotation_type/<str:pk>/", delete_quotation_type, name="delete_quotation_type"),
    path("email/<str:pk>/", email_page, name="email_page"),
    path("send_email/<str:pk>/", send_email, name="send_email"),
    path("receive_email/", receive_email, name="receive_email"),
    path("create_work_of_scope/", create_work_of_scope, name="create_work_of_scope"),
    path("update_work_of_scope/<str:pk>/", update_work_of_scope, name="update_work_of_scope"),
    path("delete_work_of_scope/<str:pk>/", delete_work_of_scope, name="delete_work_of_scope"),
    path("list_work_of_scope/", work_of_scope_list, name="create_work_of_scope_list"),
    path("list_commodity/", commodity_list, name="commodity_list"),
    path("create_commodity/", commodity_create, name="create_commodity"),
    path("update_commodity/<str:pk>/", commodity_update, name="update_commodity"),
    path("create_commodity/<str:pk>/", commodity_delete, name="delete_commodity"),

]
