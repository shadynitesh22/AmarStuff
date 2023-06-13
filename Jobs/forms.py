from django.forms import ModelForm

from .models import BookJob, Job, JobBegin, Salary, Bonus, Leave


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ("users",)


class SalaryForm(ModelForm):
    class Meta:
        model = Salary
        fields = ("__all__")


class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        exclude = ("total_leave", "leave_remaining")


class BonusForm(ModelForm):
    class Meta:
        model = Bonus
        fields = ("__all__")


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
