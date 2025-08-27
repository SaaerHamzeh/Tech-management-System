from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import *


@receiver(pre_save)
def update_customer_phone_number(sender, instance, **kwargs):
    # List of models to apply the signal to
    applicable_models = [MaintenanceInfo]  # Add model names here

    if sender.__name__ in applicable_models:  # Check if the model is in the list
        if (
            hasattr(instance, "customer")
            and hasattr(instance, "customer_phone_number")
            and instance.customer
            and not instance.customer_phone_number
        ):
            instance.customer_phone_number = instance.customer.phone


@receiver(pre_save, sender=MaintenanceInfo)
def auto_fill_maintenance_fields(sender, instance, **kwargs):
    device_fields = ["pc", "laptop", "playstation", "gamestick", "router"]

    for field in device_fields:
        device = getattr(instance, field)
        if device:
            # نسخ المشكلة إذا كانت فارغة
            if not instance.issue:
                instance.issue = device.issue

            # نسخ بيانات الزبون إذا كانت فارغة
            if not instance.customer:
                instance.customer = device.customer
                if not instance.customer_phone_number and device.customer:
                    instance.customer_phone_number = device.customer.phone
            break


# قائمة بالأجهزة التي قد يتم تعديل المشكلة بها
device_models = [PC, Laptop, PlayStation, GameStick, Router]


def update_maintenance_issue(instance):
    """تحديث المشكلة في MaintenanceInfo عند تعديل الجهاز"""

    # ربط نوع الجهاز بحقل ForeignKey في MaintenanceInfo
    device_field_map = {
        PC: "pc",
        Laptop: "laptop",
        PlayStation: "playstation",
        GameStick: "gamestick",
        Router: "router",
    }

    for model_class, field_name in device_field_map.items():
        if isinstance(instance, model_class):
            filter_kwargs = {field_name: instance}
            maintenance_record = MaintenanceInfo.objects.filter(**filter_kwargs).first()
            if maintenance_record:
                maintenance_record.issue = instance.issue
                maintenance_record.save()
            break


# ربط السيغنال مع كل موديل من الأجهزة
for model in device_models:

    @receiver(post_save, sender=model)
    def update_issue(sender, instance, **kwargs):
        update_maintenance_issue(instance)
