# Generated by Django 3.2.9 on 2022-04-27 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity_name', models.CharField(max_length=100)),
                ('commodity_description', models.CharField(max_length=100, null=True)),
                ('commodity_type', models.CharField(choices=[('GENERAL GOODS', 'GENERAL GOODS'), ('DANGEROUS_GOODS', 'DANGEROUS_GOODS'), ('CONSOLIDATION', 'CONSOLIDATION'), ('DIPLOMATIC_MAIL', 'DIPLOMATIC_MAIL')], max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=40, unique=True)),
                ('customer_email', models.EmailField(max_length=90, unique=True)),
                ('customer_phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='QuotationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOFScope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('description', models.TextField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotation_number', models.CharField(blank=True, max_length=500, null=True)),
                ('mode_of_transport', models.CharField(blank=True, choices=[('By air', 'By air'), ('By sea', 'By sea'), ('By land ', 'By land ')], db_index=True, default='By-Air', max_length=100, null=True)),
                ('airport_of_origin', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('airport_of_destination', models.CharField(blank=True, max_length=100, null=True)),
                ('no_of_shipment', models.FloatField(blank=True, max_length=20, null=True)),
                ('weights_of_shipment', models.FloatField(blank=True, help_text='Enter the weight in Kg', max_length=20, null=True)),
                ('ams_fee', models.FloatField(blank=True, max_length=20, null=True)),
                ('carrier', models.CharField(blank=True, max_length=100, null=True)),
                ('routine', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_terms', models.FloatField(blank=True, max_length=50, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('custom_clearance', models.FloatField(blank=True, default=50.0, max_length=100, null=True)),
                ('charges', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(blank=True, choices=[('Quotation Created', 'Quotation Created'), ('Quotation Email Sent', 'Quotation Email Sent'), ('Quotation Completed', 'Quotation Completed')], default='Quotation Created', max_length=200, null=True)),
                ('commodity', models.ManyToManyField(blank=True, max_length=200, to='quotation.Commodities')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotation.customers')),
                ('quotation_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='quotation.quotationtype')),
                ('users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('work_of_scope', models.ManyToManyField(blank=True, max_length=600, to='quotation.WorkOFScope')),
            ],
        ),
    ]
