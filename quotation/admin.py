from django.contrib import admin

from .models import Commodities, Customers, Quotation, QuotationType, WorkOFScope

admin.site.register(Quotation)
admin.site.register(QuotationType)
admin.site.register(WorkOFScope)
admin.site.register(Commodities)
admin.site.register(Customers)
