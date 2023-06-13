from django.urls import path

from .views import (
    book_jobs, create_job, delete_job, detail_job, job_begin_list, job_booking_delete, job_booking_update,
    job_proceed_create, job_proceed_delete, job_proceed_update, list_bookings, list_completed, list_job, list_received,
    send_booking_email, send_email_page, update_job, list_bonus, list_leave, list_salary , create_bonus , create_leave ,create_salary
)

urlpatterns = [

    path("joblist/", list_job, name="list_jobs"),
    path("joblistR/", list_received, name="list_jobsR"),
    path("joblistC/", list_completed, name="list_jobsC"),
    path("joblistB/", job_begin_list, name="joblist"),
    path("create_job/<str:pk>/", create_job, name="job-create"),
    path("update_job/<str:pk>/", update_job, name="job-update"),
    path("delete_job/<str:pk>/", delete_job, name="delete-job"),
    path("jobBegin/", job_proceed_create, name="job-begin"),
    path("update_jobBegin/<str:pk>/", job_proceed_update, name="job-updateStarted"),
    path("delete_jobStarted/<str:pk>/", job_proceed_delete, name="delete-jobStarted"),
    path("detial_jobBegin/<str:pk>/", detail_job, name="job-view"),
    path("book_job/<str:pk>/", book_jobs, name="book_job"),

    path("bonusList/", list_bonus, name="list_bonus"),
    path("salaryList/", list_salary, name="list_salary"),
    path("leaveList/", list_leave, name="list_leave"),

    path("bonusCreate/", create_bonus, name="create_bonus"),
    path("salaryCreate/", list_salary, name="create_salary"),
    path("leaveCreate/", create_leave, name="create_leave"),


    path("update_jobBookings/<str:pk>/", job_booking_update, name="update_bookings"),
    path("delete_jobBookings/<str:pk>/", job_booking_delete, name="delete_bookings"),
    path("list_job_bookings/", list_bookings, name="booking_list"),
    path("send_booking_email_page/<str:pk>/", send_email_page, name="email_page_book"),
    path("send_booking_email/<str:pk>/", send_booking_email, name="email_job")

]
