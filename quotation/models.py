from users.models import Customer

from django.db import models


class WorkOFScope(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    description = models.TextField(max_length=200, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Customers(models.Model):
    customer_name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    customer_email = models.EmailField(max_length=90, null=False, blank=False, unique=True)
    customer_phone = models.CharField(max_length=10, null=False, )

    def __str__(self):
        return self.customer_name


class Commodities(models.Model):
    GENERAL_GOODS = "GENERAL GOODS"
    DANGEROUS_GOODS = "DANGEROUS_GOODS"
    CONSOLIDATION = "CONSOLIDATION"
    DIPLOMATIC_MAIL = "DIPLOMATIC_MAIL"

    COMMODITY_TYPE = (
        (

            (GENERAL_GOODS, GENERAL_GOODS),
            (DANGEROUS_GOODS, DANGEROUS_GOODS),
            (CONSOLIDATION, CONSOLIDATION),
            (DIPLOMATIC_MAIL, DIPLOMATIC_MAIL),

        )
    )

    commodity_name = models.CharField(max_length=100, null=False)
    commodity_description = models.CharField(max_length=100, null=True)
    commodity_type = models.CharField(choices=COMMODITY_TYPE, max_length=200)

    def __str__(self):
        return self.commodity_name


class QuotationType(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name


class Quotation(models.Model):
    STATUS = (
        ("Task Created", "Task Created"),
        ("Task Email Sent", "Task Email Sent"),
        ("Task Completed", "Task Completed"),
    )
    AIRPORT_TRANSFER = "airport transfer"
    CUSTOM_CLEARANCE = "Custom clearance "
    DISPATCHED_GOOD = "Dispatched of the goods "
    AIRWAY_BILL = "Issuing of airway bill "
    AIR_FREIGHT = "Issuing of airway bill "
    DELIVERY_DESTINATION = "delivery at destination airport"

    BY_AIR = "Development"
    BY_LAND = "QA"
    BY_SEA = "Management"

    ITEM_TYPES = (
        (

            (AIRPORT_TRANSFER, AIRPORT_TRANSFER),
            (CUSTOM_CLEARANCE, CUSTOM_CLEARANCE),
            (DISPATCHED_GOOD, DISPATCHED_GOOD),
            (AIRWAY_BILL, AIRWAY_BILL),
            (AIR_FREIGHT, AIR_FREIGHT),
            (DELIVERY_DESTINATION, DELIVERY_DESTINATION)
        )
    )
    MODE_TYPES = (
        (
            (BY_AIR, BY_AIR),
            (BY_SEA, BY_SEA),
            (BY_LAND, BY_LAND)
        )

    )
    quotation_number = models.CharField(null=True, blank=True, max_length=500)
    users = models.ForeignKey(Customer, on_delete=models.CASCADE)

    mode_of_transport = models.CharField(choices=MODE_TYPES, max_length=100, null=True,
                                         blank=True, db_index=True, default="Development")
    quotation_type = models.ForeignKey(QuotationType, on_delete=models.CASCADE, null=True, blank=True)
    airport_of_origin = models.CharField(db_index=True, max_length=100, null=True, blank=True)
    airport_of_destination = models.CharField(max_length=100, null=True, blank=True, db_index=False)
    commodity = models.ManyToManyField(Commodities, max_length=200, blank=True)
    no_of_shipment = models.FloatField(max_length=20, db_index=False, null=True, blank=True)
    weights_of_shipment = models.FloatField(max_length=20, db_index=False, null=True, blank=True,
                                            help_text="Enter the weight in Kg")
    work_of_scope = models.ManyToManyField(WorkOFScope, max_length=600, blank=True)
    ams_fee = models.FloatField(max_length=20, null=True, blank=True)
    carrier = models.CharField(max_length=100, null=True, blank=True)
    routine = models.CharField(max_length=100, null=True, blank=True)
    payment_terms = models.FloatField(max_length=50, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    custom_clearance = models.FloatField(default=50.000, max_length=100, null=True, blank=True)
    charges = models.CharField(max_length=20, blank=True, null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default="Task Created")

    def __str__(self):
        return f" {self.quotation_number}:{self.customer}  "

    def save(self, *args, **kwargs):
        if self.quotation_number is None:
            quotation_number = self.quotation_number
            quotation_number = "Task1"
            exist = Quotation.objects.filter(quotation_number=quotation_number).exists()
            count = 1
            while exist:
                count += 1
                quotation_number = "Task" + str(count)
                exist = Quotation.objects.filter(quotation_number=quotation_number).exists()

            self.quotation_number = quotation_number

        super().save(*args, **kwargs)
