import email
import imaplib
import json
import threading

import easyimap as e
from Jobs.models import Job, JobBegin
from users.models import Customer, Roles

from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from core import settings
from core.decorators import allowed_users

from .forms import CommodityForm, CustomersForm, QuotationForm, QuotationTypeForm, WorkOFScopeForm
from .models import Commodities, Quotation, QuotationType, WorkOFScope
from .utils import generate_token


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class EmailReceiveThread(threading.Thread):

    def __init__(self, mail):
        self.mail = mail
        threading.Thread.__init__(self)

    def run(self):
        self.mail()


# Create your views here.

def dashboard(request):
    if request.user.is_authenticated:
        quotation = Quotation.objects.all()
        job_begin = JobBegin.objects.all()
        jobs = Job.objects.all()
        flags = jobs.filter(user=request.user)
        job = quotation.filter(status="Quotation Email Sent").count()
        quotation_type = QuotationType.objects.all()
        users = Customer.objects.all()
        roles = Roles.objects.all()
        quotation_count = quotation.count()
        job_count = job_begin.count()
        user_count = users.count()
        roles_count = roles.count()
        context = {"quotation": quotation, "quotation_type": quotation_type, "users": users, "roles": roles,
                   "quotation_count": quotation_count,
                   "user_count": user_count, "roles_count": roles_count, "email_flag": job, "jobs": jobs,
                   "flags": flags, "job_count": job_count}
        return render(request, "dashboard1.html", context)

    else:
        return redirect("login")


def quotation_list(request):
    if request.user.is_authenticated:
        quotation = Quotation.objects.all()
        quotation_type = QuotationType.objects.all()
        job = Job.objects.all()
        quotation_count = quotation.count()
        quotation_type_count = quotation_type.count()

        context = {"quotation": quotation, "quotation_type": quotation_type, "quotation_count": quotation_count,
                   "quotation_type_count": quotation_type_count, "job": job}
        return render(request, "quotation/quoatation_list.html", context)

    else:
        return redirect("login")


@allowed_users(allowed_roles=["Manger"])
def create_quotation(request):
    form = QuotationForm()
    customers = CustomersForm()
    commodity = CommodityForm()
    work_of_scope = WorkOFScopeForm()
    if request.method == "POST":

        work_of_scope = WorkOFScopeForm(request.POST)
        if work_of_scope.is_valid():
            json_commodity = work_of_scope.__dict__
            print(f"{json_commodity}")
            work_of_scope.save()
            # work_of_scope = json_commodity

        customers = CustomersForm(request.POST)
        if customers.is_valid():
            customers.save()
            messages.success(request, " Customer Created !")

        form = QuotationForm(request.POST, request.user, )
        form.instance.users = request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Quotation Created")
            return redirect("quotation_list")

        commodity = CommodityForm(request.POST)
        if commodity.is_valid():
            commodity.save()
            commodity_name = request.POST["commodity_name"]
            commodity_description = request.POST["commodity_description"]
            commodity_type = request.POST["commodity_type"]
            messages.success(request, "Commodity Created")
            HttpResponse(
                json.dumps({"commodity_name": commodity_name, "commodity_desc": commodity_description,
                            "quotation_type": commodity_type}))

    context = {"form": form, "scope": work_of_scope, "customers": customers, "commodity": commodity}
    return render(request, "quotation/quotation_create_form.html", context)


@allowed_users(allowed_roles=["Manger"])
def create_work_of_scope(request):
    work_of_scope = WorkOFScopeForm()
    if request.method == "POST":
        work_of_scope = WorkOFScopeForm(request.POST)
        if work_of_scope.is_valid():
            work_of_scope.save()
            messages.success(request, "Work of Scope Created")
        return redirect("create_work_of_scope_list")
    context = {"form": work_of_scope}
    return render(request, "quotation/work_of_scope.html", context)


@allowed_users(allowed_roles=["Manger"])
def update_work_of_scope(request, pk):
    work_of_scope = WorkOFScope.objects.get(id=pk)
    form = WorkOFScopeForm(instance=work_of_scope)
    if request.method == "POST":
        form = WorkOFScopeForm(request.POST, instance=work_of_scope)
        if form.is_valid():
            form.save()
            messages.success(request, "Work of Scope Updated")
        return redirect("create_work_of_scope_list")
    context = {"form": form}
    return render(request, "quotation/work_of_scope.html", context)


@allowed_users(allowed_roles=["Manger"])
def delete_work_of_scope(request, pk):
    work_of_scope = WorkOFScope.objects.get(id=pk)
    if request.method == "POST":
        work_of_scope.delete()
        messages.success(request, " Work of Scope deleted  !")
        return redirect("create_work_of_scope_list")

    context = {"item": work_of_scope}
    return render(request, "system/confirm_delete.html", context)


def work_of_scope_list(request):
    work_of_scope_list = WorkOFScope.objects.all()
    context = {"work_of_scope_list": work_of_scope_list}
    return render(request, "quotation/work_of_scope_list.html", context)


def commodity_list(request):
    commodity = Commodities.objects.all()
    commodity_count = commodity.count()
    context = {"commodity": commodity, "commodity_count": commodity_count}
    return render(request, "quotation/commodity_list.html", context)


@allowed_users(allowed_roles=["Manger"])
def commodity_create(request):
    form = CommodityForm()

    if request.method == "POST":
        form = CommodityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Created")
        return redirect("commodity_list")
    context = {"form": form, }
    return render(request, "quotation/commodity_create.html", context)


@allowed_users(allowed_roles=["Manger"])
def commodity_update(request, pk):
    commodity = Commodities.objects.get(id=pk)
    form = CommodityForm(instance=commodity)

    if request.method == "POST":
        form = CommodityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Commodity Updated")
        return redirect("commodity_list")
    context = {"form": form, }
    return render(request, "quotation/commodity_create.html", context)


@allowed_users(allowed_roles=["Manger"])
def commodity_delete(request, pk):
    commodity = Commodities.objects.get(id=pk)
    if request.method == "POST":
        commodity.delete()
        messages.success(request, " Commodity Deleted !")
        return redirect("commodity_list")

    context = {"item": commodity}
    return render(request, "system/confirm_delete_commodity.html", context)


def quotation_type_list(request):
    quotation_list = QuotationType.objects.all()
    context = {"quotation_list": quotation_list}
    return render(request, "quotation/quotation_type_list.html", context)


@allowed_users(allowed_roles=["Manger"])
def update_quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    form = QuotationForm(instance=quotation)

    if request.method == "POST":
        form = QuotationForm(request.POST, instance=quotation)
        if form.is_valid():
            form.save()
            messages.success(request, "Quotation has been updated ")
            return redirect("quotation_list")

    context = {"form": form}
    return render(request, "quotation/quotation_update_form.html", context)


@allowed_users(allowed_roles=["Manger"])
def delete_quotation(request, pk):
    quotation = Quotation.objects.get(id=pk)
    if request.method == "POST":
        quotation.delete()
        messages.success(request, " Quotation Deleted !")
        return redirect("quotation_list")

    context = {"item": quotation}
    return render(request, "system/confirm_delete.html", context)


def quotation_detail_view(request, pk):
    quotation = Quotation.objects.get(id=pk)
    context = {"quotation": quotation}
    return render(request, "quotation/quotation_detail.html", context)


@allowed_users(allowed_roles=["Manger"])
def create_quotation_type(request):
    form = QuotationTypeForm()
    if request.method == "POST":
        form = QuotationTypeForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, " Quotation quotation_type added")
        return redirect("quotation-list_type")

    context = {"form": form}
    return render(request, "quotation/quotation_type_create_form.html", context)


@allowed_users(allowed_roles=["Manger"])
def update_quotation_type(request, pk):
    quotation = QuotationType.objects.get(id=pk)
    form = QuotationTypeForm(instance=quotation)

    if request.method == "POST":
        form = QuotationTypeForm(request.POST, instance=quotation)
        if form.is_valid():
            form.save()
            messages.success(request, "Quotation Type updated")
            return redirect("quotation-list_type")

    context = {"form": form}
    return render(request, "quotation/quotation_type_create_form.html", context)


@allowed_users(allowed_roles=["Manger"])
def delete_quotation_type(request, pk):
    quotation = QuotationType.objects.get(id=pk)
    if request.method == "POST":
        quotation.delete()
        messages.success(request, "Quotation Deleted ")
        return redirect("quotation-list_type")

    context = {"item": quotation}
    return render(request, "system/confirm1_delete.html", context)


def send_conformation(request, pk):
    current_site = get_current_site(request)
    email_subject = "Activate your account"
    quotation = Quotation.objects.get(id=pk)
    email_body = render_to_string("email.html", {
        "user": quotation,
        "domain": current_site,
        "uid": urlsafe_base64_encode(force_bytes(pk)),
        "token": generate_token.make_token(quotation)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[quotation.customer_email.email]
                         )

    if not settings.TESTING:
        EmailThread(email).start()


@allowed_users(allowed_roles=["Manger"])
def email_page(request, pk):
    quotation = Quotation.objects.get(id=pk)

    context = {"form": quotation}
    return render(request, "email/email.html", context)


@allowed_users(allowed_roles=["Manger"])
def send_email(request, pk):
    quotation = Quotation.objects.get(id=pk)
    if request.method == "POST":
        template = render_to_string("email/email.template.html", {
            "customer_name": quotation.customer.customer_name,
            "email": quotation.customer.customer_email,
            "airport_of_origin": quotation.airport_of_origin,
            "airport_of_destination": quotation.airport_of_destination,
            "ams_fee": quotation.ams_fee,
            "mode_of_transport": quotation.mode_of_transport,
            "commodity": quotation.commodity,
            "no_of_shipment": quotation.no_of_shipment,
            "routine": quotation.routine,
            "weight of shipment": quotation.weights_of_shipment,
            "work_of_scope": quotation.work_of_scope,
            "payment_terms": quotation.payment_terms,
            "charges": quotation.charges,
            "custom": quotation.custom_clearance,
            "quotation_type": quotation.quotation_type,
            "number": quotation.quotation_number,
            "date": quotation.date,
            "time": quotation.time,

            "message": request.POST["message"],
        })

        email = EmailMessage(
            request.POST["subject"],
            template,
            settings.EMAIL_HOST_USER,
            to=[quotation.customer.customer_email]
        )
        email.content_subtype = "html"
        quotation.status = "Quotation Email Sent"
        quotation.save()
        email.fail_silently = False
        EmailThread(email).start()

        messages.success(request, " Quotation Email sent   successful !")

    return redirect("quotation_list")


my_message = []
email_data = {}


def receive_email(request):
    host = "imap.gmail.com"
    username = "np190097@gmail.com"
    password = "xioqnfgmtcaxibzv"
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")

    _, search_data = mail.search(None, "UNSEEN")
    my_message = []
    for num in search_data[0].split():

        _, data = mail.fetch(num, "(RFC822)")
        # print(data[0])
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ["subject", "to", "from", "date"]:
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data["body"] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data["html_body"] = html_body.decode()
        my_message.append(email_data)

    context = {"inbox": email_data}
    return render(request, "email/recive_email.html", context)


if __name__ == "__main__":
    my_inbox = receive_email
    print(my_inbox)


def imap_email(request):
    password = "xioqnfgmtcaxibzv"
    username = "np190097@gmail.com"
    server = e.connect("imap.gmail.com", username, password)
    server.listids()
    email = server.mail(server.listids()[0])
    title = email.title
    from_add = email.from_addr
    body = email.body
    attachments = email.attachments

    context = {"title": title, "fromAdd": from_add, "body": body, "attachments": attachments, "email": email}
    return render(request, "email/recive_email.html", context)
