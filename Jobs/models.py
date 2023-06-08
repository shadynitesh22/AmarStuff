from quotation.models import Commodities, Quotation, WorkOFScope
from users.models import Customer

from django.db import models
import datetime


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


class Payroll(models.Model):
    STATUS = (
        ("Monthly Salary", "Monthly Salary"),


    )

    status = models.CharField(max_length=200, null=True, choices=STATUS)
    user = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status} - To: {self.user.username}"

    def release_payroll(self):
        salary = self.user.salary
        salary_amount = salary.salary_amount

        release_date = salary.release_date
        today = datetime.date.today()

        if today.day < release_date:
            # Payroll will be released on the next release date of the current month
            release_month = today.month
        else:
            # Payroll will be released on the next release date of the next month
            release_month = (today.month % 12) + 1

        release_year = today.year if today.month != 12 else today.year + 1

        release_date = datetime.date(release_year, release_month, salary.release_date)

        deduction = 0

        bonus = Bonus.objects.filter(user=self.user).first()
        if bonus:
            deduction = bonus.amount

        total_salary = salary_amount - deduction
        current_salary = total_salary
        leave_days = \
        Leave.objects.filter(user=self.user, created_at__month=today.month, created_at__year=today.year).aggregate(
            total_leave=models.Sum('total_leave'))['total_leave']
        if leave_days is None:
            leave_days = 0

        if leave_days > 12:
            excess_leave = leave_days - 12
            deduction = salary_amount * (excess_leave / 100)

        total_salary = current_salary - deduction

        # Update the total_amount field in the Customer model
        self.user.total_amount += total_salary
        self.user.save()

        # Perform the necessary actions for releasing the payroll, e.g., generating payslip, sending notifications,
        # etc. ...


class Salary(models.Model):
    user = models.OneToOneField(Customer, null=False, on_delete=models.CASCADE)
    salary_amount = models.IntegerField(null=False, blank=False)
    release_date = models.PositiveSmallIntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"Salary - User: {self.user.username}"


class Bonus(models.Model):

    salary = models.ForeignKey(Salary, null=True, on_delete=models.CASCADE)
    bonus_percent = models.IntegerField(max_length=100,null=False,blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def save(self,*args,**kwargs):
        toatl_amount = self.bonus_percent % self.salary.salary_amount *100
        toatl_amount = self.amount
        super().save()

    def __str__(self):
        return f"Bonus - User: {self.user.username}"


class Leave(models.Model):
    user = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE)
    total_leave = models.IntegerField(null=False, blank=False, default=0)
    created_at = models.DateField(auto_now_add=True)


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
