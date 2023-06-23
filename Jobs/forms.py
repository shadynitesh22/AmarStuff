from django import forms
from django.forms import ModelForm

from .models import BookJob, Job, JobBegin, Salary, Bonus, Leave, Attendance


class JobForm(ModelForm):
    class Meta:
        model = Job
        exclude = ("users",)


class SalaryForm(ModelForm):
    class Meta:
        model = Salary
        fields = ("__all__")


class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        exclude = ("user",)


class LeaveForm(ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Leave
        exclude = ("total_leave_remaining", "created_at", "total_leave")


class BonusForm(ModelForm):
    class Meta:
        model = Bonus
        exclude = ("amount",)


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
