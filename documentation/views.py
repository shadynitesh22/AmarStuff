"""
All the imports are listed down below -author Nitesh Paudel
Code owner -
Licence -- BY law you are not authorized to use this code in other project whatsoever
Patented by Code Grep.com

"""
from Jobs.models import BookJob

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AccountingInformationForm, AirportDepartureForm, AirportDestinationForm, ConsignAddressForm, CurrencyForm,
    HandlingInformationForm, IssuingCarrierForm, MainPageForm, NatureOfGoodsForm, OptionalForm, ShippersAddressForm
)
# Create your views here.
from .models import ConsignAddress, MainPage, ShippersAddress


"""
This Handles functions related to Documentation Sections.. Please write
functions name in small letters to pass the flake test as well as
use "" instead of '' to describe string.
"""


def documentation_start(request, pk):
    """
    Documentation Section will begin from here
        # all the forms are listed here
        We will be using id to identify the forms
        We will use multiple Solutions to solve this problem

    """
    booked = BookJob.objects.get(id=pk)
    form = MainPageForm()
    shippers = ShippersAddressForm()
    consign = ConsignAddressForm()
    accounts = AccountingInformationForm()
    airport_destination = AirportDestinationForm()
    airport_departure = AirportDepartureForm()
    handling_info = HandlingInformationForm()
    currency = CurrencyForm()
    nature = NatureOfGoodsForm()
    issues = IssuingCarrierForm()
    optional = OptionalForm()

    """
    Form will be handled here as you can see we get the post request and check the id
    To execute a particular  form
     """
    if request.method == "POST":
        if request.POST.get("form_type") == "shippers":
            company_name = request.POST["company_name"]
            address = request.POST["address"]

            shippers = ShippersAddress.objects.create(
                company_name=company_name,
                address=address
            )
            shippers.save()
            messages.success(request, "Shippers address created !!")

        elif request.POST.get("form_type") == "consign":
            company_names = request.POST["company_names"]
            addresss = request.POST["addresss"]
            consign = ConsignAddress.objects.create(
                company_names=company_names,
                addresss=addresss
            )
            consign.save()
            messages.success(request, "Consign address created !!")

        elif request.POST.get("form_type") == "accounts":
            accounts = AccountingInformationForm(request.POST)
            if accounts.is_valid():
                accounts.save()
                messages.success(request, "Accounts created !!")

        elif request.POST.get("form_type") == "airport_dept":
            airport_departure = AirportDepartureForm(request.POST)
            if airport_departure.is_valid():
                airport_departure.save()
                messages.success(request, "Airport Dept created !!")

        elif request.POST.get("form_type") == "airport_dest":
            airport_destination = AirportDestinationForm(request.POST)
            if airport_destination.is_valid():
                airport_destination.save()
                messages.success(request, "Airport Destination created !!")

        elif request.POST.get("form_type") == "handling_info":
            handling_info = HandlingInformationForm(request.POST)
            if handling_info.is_valid():
                handling_info.save()
                messages.success(request, "handling_info created !!")

        elif request.POST.get("form_type") == "currency":
            currency = CurrencyForm(request.POST)
            if currency.is_valid():
                currency.save()
                messages.success(request, "Currency created !!")

        elif request.POST.get("form_type") == "nature":
            nature = NatureOfGoodsForm(request.POST)
            if nature.is_valid():
                nature.save()
                messages.success(request, "Nature created !!")

        elif request.POST.get("form_type") == "issuing":
            issues = IssuingCarrierForm(request.POST)
            if issues.is_valid():
                issues.save()
                messages.success(request, "Issuing Carrier created !!")

        elif request.POST.get("form_type") == "optional":
            optional = OptionalForm(request.POST)
            if optional.is_valid():
                optional.save()
                messages.success(request, "Optional created !!")

        elif request.POST.get("form_type") == "main_form":
            form = MainPageForm(request.POST)
            if form.is_valid():
                bookeded = form.cleaned_data.get("booked")
                print(bookeded)
                issued_by = form.cleaned_data.get("issued_by")
                print(issued_by)
                bookeded = booked
                booked.save()
                issued_by = request.user
                issued_by.save()
                form.save()
                return redirect("list-documentation")
            """
                There is a lot of elif and can be hard to identify or check
                we can use prefix for better understanding

                """

    context = {"form": form, "optional": optional, "issues": issues, "nature": nature,
               "currency": currency, "handling": handling_info, "consign": consign, "shippers": shippers,
               "accounts": accounts, "airport_destination": airport_destination,
               "airport_departure": airport_departure}
    return render(request, "documentation/documents-create.html", context)


def list_documents(request):
    """
    This is a list view which lists all the data,notice there are no filters because you want every data
    we can set up order by -- setting this up needs you to put ordering in models
    """
    documentation = MainPage.objects.all()
    context = {"documents": documentation}
    return render(request, "documentation/documentation-list.html", context)


def detail_documents(request, pk):
    """
    This functions returns a paticular object
    Django provide class based view for this propose but this approach is faster and abstraction is low .

    """
    detail_documentation = MainPage.objects.get(id=pk)
    context = {"mawb": detail_documentation}
    return render(request, "documentation/documentation_detail.html", context)


def form_update(request, pk):
    """
    This is a basic Update view
    Updates models base on django forms

    """
    main_page = MainPage.objects.get(id=pk)
    form = MainPageForm(instance=main_page)
    if request.method == "POST":
        form = MainPageForm(request.POST, instance=main_page)
        if form.is_valid():
            user = form.cleaned_data.get("booked")
            form.save()
            messages.success(request, f"Your data has been saved ")
        return redirect("list-documentation")
    context = {"form": form}
    return render(request, "documentation/documentation-edit.html", context)


def delete_form(request, pk):
    """
    Deletes the object . Basically a deleted view
    """

    main_page = MainPage.objects.get(id=pk)
    if request.method == "POST":
        main_page.delete()
        messages.success(request, f"You have successfully deleted ")
        return redirect("list-documentation")
    context = {"item": main_page}
    return render(request, "documentation/documentation-delete.html", context)


def create_from_multiple(request):
    """

    This is approach to solve the if else conditional loop in the view
    by looping through items
    but this also cause a problem adding more steps in decripting the list
    so we will use lookup directory to the work in another view
    """
    # display forms
    display_shippers = ShippersAddressForm()
    display_consign = ConsignAddressForm()
    display_accounts = AccountingInformationForm()
    display_airport_destination = AirportDestinationForm()
    display_airport_departure = AirportDepartureForm()
    display_handling_info = HandlingInformationForm()
    display_currency = CurrencyForm()
    display_nature = NatureOfGoodsForm()
    display_issues = IssuingCarrierForm()
    display_optional = OptionalForm()
    form_list_display = [display_shippers, display_consign, display_accounts, display_airport_destination,
                         display_airport_departure, display_handling_info, display_currency,
                         display_nature, display_issues, display_optional]

    # Create Form
    shippers = ShippersAddressForm(request.POST)
    consign = ConsignAddressForm(request.POST)
    accounts = AccountingInformationForm(request.POST)
    airport_destination = AirportDestinationForm(request.POST)
    airport_departure = AirportDepartureForm(request.POST)
    handling_info = HandlingInformationForm(request.POST)
    currency = CurrencyForm(request.POST)
    nature = NatureOfGoodsForm(request.POST)
    issues = IssuingCarrierForm(request.POST)
    optional = OptionalForm(request.POST)

    form_list = [shippers, consign, accounts, airport_destination, airport_departure, handling_info, currency, nature,
                 issues, optional]

    if request.method == "POST":
        for i in form_list:
            if i.is_valid():
                i.save()
                messages.success(request, "Created ")
                return redirect(request, "list-documentation")
            else:
                messages.error(request, f" Error has occurred {i.errors}")
                break
    context = {'list': form_list_display}
    return render(request, "documentation/documentation-create", context)


def shippers_form(request):
    """
    This was a format I was using to solve the multiple forms by calling this function
    in the forms but the redirect gave problems because it needs foreign key for redirection

    """
    if request.method == "POST":
        company_name = request.POST["company_name"]
        address = request.POST["address"]
        shippers = ShippersAddress.objects.create(
            company_name=company_name,
            address=address
        )
        shippers.save()
        messages.success(request, "Successfully Created ", fail_silently=False)

        return redirect('documentation-form')

    return HttpResponseRedirect(reverse('documentation-form'))


def consing_pass(request):
    """
    Tried this function but had some implications
    """
    consign = ConsignAddressForm()
    if request.method == "POST":
        pass
    context = {
        "consign": consign
    }
    return render(request, "documentation/documentation-create", context)


def shippers_pass(request):
    shippers = ShippersAddressForm()
    if request.method == "POST":
        pass
    context = {
        "shippers": shippers
    }
    return render(request, "documentation/documentation-create", context)
