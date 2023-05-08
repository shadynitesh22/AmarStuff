from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget, forms
from django.forms import ModelForm

from .models import Commodities, Customers, Quotation, QuotationType, WorkOFScope


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class QuotationForm(ModelForm):
    AIRPORT_TRANSFER = "airport transfer"
    CUSTOM_CLEARANCE = "Custom clearance "
    DISPATCHED_GOOD = "Dispatched of the goods "
    AIRWAY_BILL = "Issuing of airway bill "
    AIR_FREIGHT = "Issuing of airway bill "
    DELIVERY_DESTINATION = "delivery at destination airport"

    BY_AIR = "By air"
    BY_LAND = "By land "
    BY_SEA = "By sea"

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
    date = forms.DateField(widget=AdminDateWidget())
    time = forms.TimeField(widget=AdminTimeWidget)

    class Meta:
        model = Quotation
        exclude = ("users", "status")
        widgets = {
            "date": AdminDateWidget(),
            "time": AdminTimeWidget(),

        }


class QuotationTypeForm(ModelForm):
    class Meta:
        model = QuotationType
        fields = "__all__"


class WorkOFScopeForm(ModelForm):
    class Meta:
        model = WorkOFScope
        fields = "__all__"


class CustomersForm(ModelForm):
    class Meta:
        model = Customers
        fields = "__all__"


class CommodityForm(ModelForm):
    class Meta:
        model = Commodities
        fields = "__all__"
