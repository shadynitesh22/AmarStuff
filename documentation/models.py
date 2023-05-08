

from Jobs.models import BookJob
from quotation.models import Commodities
from users.models import Customer

from django.db import models


class ShippersAddress(models.Model):
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} with the  {self.address}"


class ConsignAddress(models.Model):
    company_names = models.CharField(max_length=200, null=True, blank=False)
    addresss = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return f"{self.company_names} with the {self.addresss}"


class IssuingCarrier(models.Model):
    carrier_name = models.CharField(max_length=100, blank=True, null=True)
    carrier_agent_country = models.CharField(max_length=100, blank=True, null=True)
    carrier_agent_iata_code = models.CharField(max_length=100, blank=True, null=True)
    carrier_agent_account_no = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.carrier_name} with the account no {self.carrier_agent_account_no}"


class AccountingInformation(models.Model):
    payments_types_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.payments_types_name}"


class AirportOfDeparture(models.Model):
    requested_routing = models.BooleanField(default=False, blank=True, null=True)
    to_airport = models.CharField(max_length=100, blank=True, null=True)
    to_airline = models.CharField(max_length=100, blank=True, null=True)
    to_airline_prefix_number = models.CharField(max_length=100, blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     self.to_airport = [f"{self.to_airport}"]
    #     self.to_airline_ = [f"{self.to_airline}"]
    #     self.to_airline_prefix_number = [f"{self.to_airline_prefix_number}"]
    #     return [f"{self.to_airport}, {self.to_airline_}, {self.to_airline_prefix_number}"]

    def __str__(self):
        return f"{self.to_airline} to the airport {self.to_airport} "


class AirportDestination(models.Model):
    destination_airport = models.CharField(max_length=100, null=True, blank=True)
    requested_flight_date = models.DateField(null=True, blank=True)
    amt_of_insurance = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"{self.destination_airport} with the flight date {self.requested_flight_date}"


class HandlingInformation(models.Model):
    handling_info = models.TextField(max_length=500, null=True, blank=True)
    goods_noofpcsrcp = models.FloatField(max_length=20, null=True, blank=True)
    goods_grossweight = models.FloatField(max_length=20, null=True, blank=True)
    goods_weightunit = models.FloatField(max_length=20, null=True, blank=True)
    commodity = models.ForeignKey(Commodities, on_delete=models.DO_NOTHING)
    goods_chargableweight = models.FloatField(max_length=100, null=True, blank=True)
    goods_ratecharge = models.FloatField(max_length=100, null=True, blank=True)
    goods_to = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.goods_to} with the gross weight {self.goods_grossweight}"


class NatureOfGoods(models.Model):
    goods_natureandquantity = models.FloatField(max_length=20, null=True)
    weightcharge_prepaid = models.CharField(max_length=200, null=True, blank=True)
    weightcharge_collect = models.CharField(max_length=200, null=True, blank=True)
    valuationcharge_prepaid = models.CharField(max_length=200, null=True, blank=True)
    tax_prepaid = models.FloatField(max_length=200, null=True, blank=True)
    tax_collect = models.FloatField(max_length=20, null=True, blank=True)
    charges_other = models.CharField(max_length=100, null=True, blank=True)
    totalotherchargesdueagent_prepaid = models.CharField(max_length=200, null=True, blank=True)
    totalotherchargesdueagent_collect = models.CharField(max_length=200, null=True, blank=True)
    totalotherchargesduecarrier_prepaid = models.CharField(max_length=200, null=True, blank=True)
    totalotherchargesduecarrier_collect = models.CharField(max_length=200, null=True, blank=True)
    total_prepaid = models.FloatField(max_length=200, null=True, blank=True)
    total_collect = models.FloatField(max_length=200, null=True, blank=True)
    currencyconversionrate = models.FloatField(max_length=200, null=True, blank=True)
    ccchargesindestcurrency = models.FloatField(max_length=200, null=True, blank=True)
    executed_on_date = models.DateField(null=True, blank=True)
    signature_issuingcarrieroragent = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return f"{self.total_prepaid} with the date {self.executed_on_date}"


class Currency(models.Model):
    Payment_type = (
        ("PPD", "PPD"),
        ("COLL", "COLL"),

    )
    currency_code = models.CharField(max_length=100, null=True, blank=True)
    cngs_code = models.CharField(max_length=100, null=True, blank=True)
    wt_val_payment_type = models.CharField(max_length=100, null=True, blank=True, choices=Payment_type)
    declared_val_for_carriage = models.CharField(max_length=100, null=True, blank=True)
    declared_val_for_customs = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.currency_code}"


class OptionalShippingInformation(models.Model):
    TYPE = (
        ("PPD", "PPD"),
        ("COLL", "COLL"),

    )

    reference_number = models.CharField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=10, null=False, blank=True)
    declared_value_for_change = models.CharField(max_length=200, null=True, blank=True)
    declared_value_for_customer = models.CharField(max_length=100, null=True, blank=True)
    CHG = models.CharField(max_length=200, choices=TYPE, default="PPD")

    def __str__(self):
        return f"{self.reference_number}"


class MainPage(models.Model):
    booked = models.ManyToManyField(BookJob)
    shippers_address = models.ManyToManyField(ShippersAddress)
    consign_address = models.ManyToManyField(ConsignAddress)
    issuing_carrier = models.ManyToManyField(IssuingCarrier)
    accounting_information = models.ManyToManyField(AccountingInformation)
    airport_of_departure = models.ManyToManyField(AirportOfDeparture)
    airport_of_destination = models.ManyToManyField(AirportDestination)
    handling_information = models.ManyToManyField(HandlingInformation)
    nature_of_goods = models.ManyToManyField(NatureOfGoods)
    currency = models.ManyToManyField(Currency)
    issued_by = models.ManyToManyField(Customer)
    shipping = models.ManyToManyField(OptionalShippingInformation)

    def __str__(self):
        return f"{self.booked}{self.issued_by}"

    def _get_json(self):
        response = {"booked": self.booked, "carrier_name_and_city": self.carrier_name_and_city,
                    "issued_by": self.consigin_by, "accounting_information": self.accounting_information,
                    "agents_aita_code": self.agents_aita_code, "shipping": []}
        ship_details = self.shipping.all()
        for ship_details in ship_details:
            response["shipping"].append(
                {
                    "reference_number": ship_details.reference_number,
                    "currency": ship_details.currency,
                    "declared_value_for_change": ship_details.declared_value_for_change,
                    "declared_value_for_customer": ship_details.declared_value_for_customer,
                    "CHG": ship_details.CHG
                }
            )
        return response
