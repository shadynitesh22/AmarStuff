from django.contrib import admin

from .models import (
    AccountingInformation, AirportDestination, AirportOfDeparture, ConsignAddress, Currency, HandlingInformation,
    IssuingCarrier, MainPage, NatureOfGoods, OptionalShippingInformation, ShippersAddress
)

# Register your models here.

admin.site.register(MainPage)
admin.site.register(AirportDestination)
admin.site.register(AirportOfDeparture)
admin.site.register(ConsignAddress)
admin.site.register(ShippersAddress)
admin.site.register(HandlingInformation)
admin.site.register(NatureOfGoods)
admin.site.register(AccountingInformation)
admin.site.register(IssuingCarrier)
admin.site.register(OptionalShippingInformation)
admin.site.register(Currency)
