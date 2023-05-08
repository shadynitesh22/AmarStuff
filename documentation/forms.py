from django.forms import ModelForm

from .models import (
    AccountingInformation, AirportDestination, AirportOfDeparture, ConsignAddress, Currency, HandlingInformation,
    IssuingCarrier, MainPage, NatureOfGoods, OptionalShippingInformation, ShippersAddress
)


class MainPageForm(ModelForm):
    class Meta:
        model = MainPage
        exclude = ("booked", "issued_by")


class AccountingInformationForm(ModelForm):
    class Meta:
        model = AccountingInformation
        fields = "__all__"


class AirportDestinationForm(ModelForm):
    class Meta:
        model = AirportDestination
        fields = "__all__"


class AirportDepartureForm(ModelForm):
    class Meta:
        model = AirportOfDeparture
        fields = "__all__"


class HandlingInformationForm(ModelForm):
    class Meta:
        model = HandlingInformation
        fields = "__all__"


class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = "__all__"


class ShippersAddressForm(ModelForm):
    class Meta:
        model = ShippersAddress
        fields = "__all__"


class ConsignAddressForm(ModelForm):
    class Meta:
        model = ConsignAddress
        fields = "__all__"


class NatureOfGoodsForm(ModelForm):
    class Meta:
        model = NatureOfGoods
        fields = "__all__"


class IssuingCarrierForm(ModelForm):
    class Meta:
        model = IssuingCarrier
        fields = "__all__"


class OptionalForm(ModelForm):
    class Meta:
        model = OptionalShippingInformation
        fields = "__all__"
