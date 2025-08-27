import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class CustomerFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="date_created", lookup_expr="gte")
    # end_date = DateFilter(field_name="date_created", lookup_expr="lte")
    # note = CharFilter(field_name="note", lookup_expr="icontains")

    class Meta:
        model = Customer
        fields = ["name", "phone"]


class TechnicianFilter(django_filters.FilterSet):

    class Meta:
        model = Technician
        fields = ["name", "phone"]


class MaintenanceInfoFilter(django_filters.FilterSet):

    class Meta:
        model = MaintenanceInfo
        fields = "__all__"
        exclude = [
            "laptop",
            "playstation",
            "issue",
            "customer_phone_number",
            "date_created",
            "maintenance_time",
            "maintenance_number",
            "maintenance_report",
            "handover_date",
        ]


class SalesFilter(django_filters.FilterSet):

    class Meta:
        model = Sales
        fields = "__all__"
        exclude = [
            "quantity",
            "received_amount",
            "status",
            "warranty",
            "serial_number",
            "notes",
            "cost",
            "description",
            "purchases",
            "internet_subscription",
            "arrival",
        ]


class PaymentsFilter(django_filters.FilterSet):

    class Meta:
        model = Payments
        fields = "__all__"
        exclude = [
            "quantity",
            "status",
            "warranty",
            "serial_number",
            "notes",
            "description",
        ]
