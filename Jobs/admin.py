from django.contrib import admin

from .models import BookJob, Job, JobBegin

# Register your models here.

admin.site.register(Job)
admin.site.register(JobBegin)
admin.site.register(BookJob)
