from django.forms import ModelForm

from .models import BookJob, Job, JobBegin


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ("users",)


class JobProceedForm(ModelForm):
    class Meta:
        model = JobBegin
        exclude = ("job_number", "status")

    def __init__(self, *args, **kwargs):
        super(JobProceedForm, self).__init__(*args, **kwargs)


class JobEditForm(ModelForm):
    class Meta:
        model = JobBegin
        exclude = ("job_number",)


class JobBookForm(ModelForm):
    class Meta:
        model = BookJob
        exclude = ("jobs",)
