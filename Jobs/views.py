import threading

from users.models import Customer

from django.contrib import messages
from django.core.mail import EmailMessage
from django.forms.models import inlineformset_factory
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from core import settings
from core.decorators import allowed_users

from .forms import JobBookForm, JobEditForm, JobForm, JobProceedForm, BonusForm, LeaveForm, SalaryForm
from .models import BookJob, Job, JobBegin
from .models import Salary, Bonus, Leave


# Create your views here.


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def list_salary(request):
    salary = Salary.objects.all()
    context = {"salary": salary}
    return render(request, "payroll/payroll.list.html", context)


def list_leave(request):
    leave = Leave.objects.all()
    context = {"leave": leave}
    return render(request, "payroll/leave.list.html", context)


def list_bonus(request):
    bonus = Bonus.objects.all()
    context = {"bonus": bonus}
    return render(request, "payroll/bonus.html", context)


def create_bonus(request):
    bonusForm = BonusForm()
    if request.method == "POST":
        bonusForm = BonusForm(request.POST)
        if bonusForm.is_valid():
            bonusForm.save()
            messages.success(request, "Bonus created")
        return redirect("bonus_list")
    context = {"form": bonusForm}
    return render(request, "payroll/bonus_create.html", context)


def create_leave(request):
    leave_form = LeaveForm()
    if request.method == "POST":
        leave_form = LeaveForm(request.POST)
        if leave_form.is_valid():
            leave_form.save()
            messages.success(request, "Leave created")
        return redirect("list_leave")
    context = {"form": leave_form}
    return render(request, "payroll/leave_create.html", context)


def create_salary(request):
    salary_form = SalaryForm()
    if request.method == "POST":
        salary_form = SalaryForm(request.POST)
        if salary_form.is_valid():
            salary_form.save()
            messages.success(request, "Leave created")
        return redirect("salary_list")
    context = {"form": salary_form}
    return render(request, "payroll/create_salary.html", context)


def list_job(request):
    jobs = Job.objects.all()
    job = jobs.filter(status="Quotation Sent")
    context = {"jobs": jobs, "job": job}
    return render(request, "jobs/job_list.html", context)


def list_received(request):
    jobs = Job.objects.all()
    job = jobs.filter(status="Quotation Received")
    context = {"jobs": jobs, "job": job}
    return render(request, "jobs/job_list.html", context)


def list_completed(request):
    jobs = Job.objects.all()
    job = jobs.filter(status="Quotation Completed")
    context = {"jobs": jobs, "job": job}
    return render(request, "jobs/job_listC.html", context)


def create_job(request, pk):
    job_form_set = inlineformset_factory(Customer, Job, fields=("quotation", "status",), extra=2)
    customer = Customer.objects.get(id=pk)
    formset = job_form_set(queryset=Job.objects.none(), instance=customer)
    # form = OrderForm(initial={"customer":customer})
    if request.method == "POST":
        # print("Printing POST:", request.POST)

        formset = job_form_set(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("list_jobs")

    context = {"form": formset}
    return render(request, "jobs/create_job.html", context)


def update_job(request, pk):
    jobs = Job.objects.get(id=pk)
    form = JobForm(instance=jobs)
    if request.method == "POST":
        form = JobForm(request.POST, instance=jobs)
        if form.is_valid():
            form.save()
            status = form.cleaned_data.get("status")
            if status == "Quotation Sent":
                return redirect("list_jobs")

            if status == "Quotation Received":
                return redirect("list_jobsR")

            if status == "Quotation Completed":
                return redirect("list_jobsC")

    context = {"form": form}
    return render(request, "jobs/update_job.html", context)


def delete_job(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == "POST":
        job.delete()
        if job.status == "Quotation Sent":
            return redirect("list_jobs")
        if job.status == "Quotation Received":
            return redirect("list_jobsR")
        if job.status == "Quotation Completed":
            return redirect("list_jobsC")
    context = {"item": job}
    return render(request, "system/delete_jobs.html", context)


@allowed_users(allowed_roles=["Manager"])
def job_proceed_create(request):
    form = JobProceedForm()
    if request.method == "POST":
        form = JobProceedForm(request.POST)
        if form.is_valid():
            quotation = form.cleaned_data.get("quotation")

            quotation.status = "Quotation Completed"
            quotation.save()
            form.save()
            messages.success(request, "Job Created")
        return redirect("joblist")

    context = {"form": form, }
    return render(request, "jobs/Job_begin.html", context)


@allowed_users(allowed_roles=["Manager"])
def job_proceed_update(request, pk):
    job_began = JobBegin.objects.get(id=pk)
    form = JobEditForm(instance=job_began)
    if request.method == "POST":
        form = JobEditForm(request.POST, instance=job_began)
        if form.is_valid():
            form.save()
            messages.success(request, "Job Has been updated !!!")
        return redirect("joblist")

    context = {"form": form}
    return render(request, "jobs/jobUpdate.html", context)


@allowed_users(allowed_roles=["Manager"])
def job_proceed_delete(request, pk):
    job_began = JobBegin.objects.get(id=pk)
    if request.method == "POST":
        job_began.delete()
        return redirect("joblist")
    messages.success(request, "Successfully Deleted !!")
    context = {"item": job_began}
    return render(request, "system/delete_startedJob.html", context)


def job_begin_list(request):
    jobs = JobBegin.objects.all()
    context = {"jobs": jobs}
    return render(request, "jobs/job_listB.html", context)


def detail_job(request, pk):
    jobs = JobBegin.objects.get(id=pk)
    context = {"jobs": jobs}
    return render(request, "jobs/detailJob.html", context)


@allowed_users(allowed_roles=["Manager"])
def book_jobs(request, pk):
    jobs = JobBegin.objects.get(id=pk)
    form = JobBookForm()
    if request.method == "POST":
        form = JobBookForm(request.POST)
        if form.is_valid():
            form.instance.jobs = jobs
            forms = form.save(commit=False)
            jobs.status = "Job Booked"
            jobs.save()

            forms.save()
            messages.success(request, "Booking Created !!")
            return redirect("booking_list")

    context = {"form": form}
    return render(request, "jobs/bookJob.html", context)


@allowed_users(allowed_roles=["Manager"])
def job_booking_update(request, pk):
    job_began = BookJob.objects.get(id=pk)
    form = JobBookForm(instance=job_began)
    if request.method == "POST":
        form = JobBookForm(request.POST, instance=job_began)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking Updated !!")
        return redirect("booking_list")

    context = {"form": form}
    return render(request, "jobs/updateJob.html", context)


@allowed_users(allowed_roles=["Manager"])
def job_booking_delete(request, pk):
    job_began = BookJob.objects.get(id=pk)
    if request.method == "POST":
        job_began.delete()
        return redirect("booking_list")
    messages.success(request, "Successfully Deleted ")
    context = {"item": job_began}
    return render(request, "system/delete_BookedJob.html", context)


def list_bookings(request):
    bookings = BookJob.objects.order_by("jobs")
    context = {"bookings_list": bookings}
    return render(request, "jobs/booking_list.html", context)


@allowed_users(allowed_roles=["Manager"])
def send_email_page(request, pk):
    book_job = BookJob.objects.get(id=pk)
    context = {"form": book_job}
    return render(request, "email/email_bookings.html", context)


@allowed_users(allowed_roles=["Manager"])
def send_booking_email(request, pk):
    bookings = BookJob.objects.get(id=pk)
    if request.method == "POST":
        template = render_to_string("email/email_bookings.template.html", {
            "number": request.POST["number"],
            "pieces": bookings.pieces,
            "commodity": bookings.jobs.commodities,
            "destination": bookings.airport_destination,
            "message": request.POST["message"],

        })
        multi_email = bookings.email
        multi = multi_email.split(",")

        email = EmailMessage(
            request.POST["subject"],
            template,
            settings.EMAIL_HOST_USER,
            to=multi
        )
        bookings.jobs.status = "Job Booking Email Sent"
        bookings.jobs.save()
        email.fail_silently = False
        EmailThread(email).start()

        messages.success(request, " Job Booking email sent   successful !")

    return redirect("booking_list")


def release_payroll(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        payroll_type = request.POST.get('payroll_type')

        # Retrieve the user and payroll objects based on the selected user ID
        user = Customer.objects.get(id=user_id)
        payroll = Payroll.objects.create(status=payroll_type, user=user)

        # Release the payroll
        payroll.release_payroll()

        # Redirect to a success page or do any other necessary actions
        return redirect('success')

    # Render the payroll release form
    return render(request, 'release_payroll.html')

def success(request):
    # Render a success page
    return render(request, 'success.html')
