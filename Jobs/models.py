from quotation.models import Commodities, Quotation, WorkOFScope
from users.models import Customer

from django.db import models


class Job(models.Model):
    STATUS = (
        ("Quotation Sent", "Quotation Sent"),
        ("Quotation Received", "Quotation Received"),
        ("Quotation Completed", "Quotation Completed"),
    )
    quotation = models.OneToOneField(Quotation, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    user = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} -To:{self.quotation.customer.customer_name}"


class JobBegin(models.Model):
    STATUS = (
        ("Job Created", "Job Created"),
        ("Job Booked", "Job Booked"),
        ("Job Booking Email Sent", "Job Booking Email Sent"),
    )
    quotation = models.ForeignKey(Quotation, null=False, on_delete=models.CASCADE)
    shippers_address = models.CharField(max_length=200, null=False)
    consign_address = models.CharField(max_length=200, null=False)
    Piece = models.FloatField(max_length=200)
    weight = models.FloatField(max_length=200, help_text="Enter the weight in kg")
    commodities = models.ManyToManyField(Commodities, max_length=600)
    dimension_height = models.FloatField(max_length=200, null=True, )
    dimension_weight = models.FloatField(max_length=200, null=True, )
    dimension_breadth = models.FloatField(max_length=200, null=True)
    dimension_pieces = models.FloatField(max_length=200, null=True)
    job_number = models.CharField(max_length=200, null=True, blank=True)
    work_of_scope = models.ManyToManyField(WorkOFScope, max_length=200)
    status = models.CharField(max_length=200, null=True, blank=True, choices=STATUS, default="Job Created")

    def save(self, *args, **kwargs):
        if self.job_number is None:
            job_number = self.job_number
            job_number = "JOB#123-"
            exist = JobBegin.objects.filter(job_number=job_number).exists()
            count = 1
            while exist:
                count += 1
                job_number = "JOB#00-" + str(count)
                exist = JobBegin.objects.filter(job_number=job_number).exists()

            self.job_number = job_number

        super().save(*args, **kwargs)

    def __str__(self):
        return self.job_number


class BookJob(models.Model):
    jobs = models.OneToOneField(JobBegin, on_delete=models.CASCADE, null=True, blank=True)
    air_bill_number = models.CharField(max_length=200, null=False)
    airport_destination = models.CharField(max_length=200, null=False)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    pieces = models.FloatField(null=True)
    weight_of_shipment = models.FloatField(max_length=10, null=False)
    carrier = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.air_bill_number} Booked"

    class Meta:
        ordering = ("jobs",)
