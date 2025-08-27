from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from .models import *
from django import forms
from dal import autocomplete


class CustomerForm(forms.Form):
    existing_customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False,
        label="اختر زبون موجود",
        widget=autocomplete.ModelSelect2(
            url="customer-autocomplete",
            attrs={"data-placeholder": "ابحث عن اسم الزبون", "style": "width: 100%;"},
        ),
    )

    new_name = forms.CharField(required=False, label="اسم الزبون الجديد")
    new_phone = forms.CharField(required=False, label="رقم الهاتف الجديد")


class TechnicianForm(ModelForm):
    class Meta:
        model = Technician
        fields = "__all__"


class PCForm(ModelForm):
    issue = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )

    class Meta:
        model = PC
        fields = "__all__"
        exclude = ["device_type", "customer"]


class pcRAMForm(forms.ModelForm):
    class Meta:
        model = pcRAM
        exclude = ("pc",)


class pcHardForm(forms.ModelForm):
    class Meta:
        model = pcHARD
        exclude = ("pc",)


pcRAMFormSet = inlineformset_factory(
    PC, pcRAM, fields=("ram_type", "ram_size", "ram_serial_number"), extra=4
)
pcHardFormSet = inlineformset_factory(
    PC, pcHARD, fields=("hard_type", "hard_size", "hard_serial_number"), extra=4
)


class LaptopForm(ModelForm):

    issue = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )

    class Meta:
        model = Laptop
        fields = "__all__"
        exclude = ["device_type", "customer"]


class laptopRAMForm(forms.ModelForm):
    class Meta:
        model = laptopRAM
        exclude = ("laptop",)


class laptopHardForm(forms.ModelForm):
    class Meta:
        model = laptopHARD
        exclude = ("laptop",)


laptopRAMFormSet = inlineformset_factory(
    Laptop, laptopRAM, fields=("ram_type", "ram_size", "ram_serial_number"), extra=4
)
laptopHardFormSet = inlineformset_factory(
    Laptop, laptopHARD, fields=("hard_type", "hard_size", "hard_serial_number"), extra=4
)


class RouterForm(ModelForm):

    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )

    class Meta:
        model = Router
        fields = "__all__"
        exclude = ["device_type", "customer"]


class GameStickForm(ModelForm):
    # serial_number = forms.CharField(required=False)
    # issue = forms.CharField(required=False)
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )

    class Meta:
        model = GameStick
        fields = "__all__"
        exclude = ["device_type", "customer"]


class PlaystationForm(ModelForm):

    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 30,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )
    accessories = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 45,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        ),
        required=False,
    )

    class Meta:
        model = PlayStation
        fields = "__all__"
        exclude = ["device_type", "customer"]


class MaintenanceInfoForm(forms.ModelForm):

    maintenance_report = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "cols": 30,
                "style": "resize: none;",
            }
        ),
        required=False,
    )

    class Meta:
        model = MaintenanceInfo
        exclude = [
            "customer",
            "maintenance_number",
            "date_created",
        ]  # نستثني customer لأنه بنعالجه يدويًا


class SalesForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 60,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        )
    )
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 60,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        )
    )

    class Meta:
        model = Sales
        fields = "__all__"


class PaymentsForm(ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 60,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        )
    )
    notes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,  # height
                "cols": 60,  # width
                "style": "resize: none;",  # optional: to disable resizing
            }
        )
    )

    class Meta:
        model = Payments
        fields = "__all__"
