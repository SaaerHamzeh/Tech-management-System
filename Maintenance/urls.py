from django.urls import path
from . import views
from dal import autocomplete
from .views import CustomerAutocomplete

urlpatterns = [
    path("", views.dashboard, name="alshaar dashboard"),
    path("maintenance devices", views.devicesMaintenance, name="devices"),
    path("create maintenance order/", views.maintenance_form, name="maintenance_form"),
    path("alshaar customers/", views.customers, name="customers"),
    path("alshaar technicians/", views.technicians, name="technicians"),
    # ---------------get-device-form------------------
    path("get-device-form/", views.get_device_form, name="get_device_form"),
    # ::::::::::::::create::::::::::::::
    path("create sale/", views.sales_form, name="sales"),
    path("create payment/", views.payments_form, name="payments"),
    path("create pc/", views.createPC, name="create_pc"),
    path("create laptop/", views.createLaptop, name="create_laptop"),
    path("create PS/", views.createPS, name="create_PS"),
    path("create router/", views.createRouter, name="create_router"),
    path("create PS stick/", views.createPsStick, name="create_PS_stick"),
    path("create customer/", views.createCustomer, name="create_customer"),
    path("create technician/", views.createTechnician, name="create_technician"),
    # ::::::::::::::update::::::::::::::
    path(
        "update maintenance order/<str:pk>/",
        views.updateMaintenance,
        name="update_order",
    ),
    path("update sale/<str:pk>/", views.updateSale, name="update_sale"),
    path("update payment/<str:pk>/", views.updatePayment, name="update_payment"),
    path("update pc/<str:pk>/", views.updatePC, name="update_pc"),
    path("update laptop/<str:pk>/", views.updateLaptop, name="update_laptop"),
    path(
        "update laptop ram/<str:pk>/", views.updateLaptopRAM, name="update_laptop_ram"
    ),
    path(
        "update laptop hard/<str:pk>/",
        views.updateLaptopHARD,
        name="update_laptop_hard",
    ),
    path("update pc ram/<str:pk>/", views.updatepcRAM, name="update_pc_ram"),
    path("update pc hard/<str:pk>/", views.updatepcHARD, name="update_pc_hard"),
    path("update PS/<str:pk>/", views.updatePS, name="update_PS"),
    path("update router/<str:pk>/", views.updateRouter, name="update_router"),
    path("update PS stick/<str:pk>/", views.updatePsStick, name="update_PS_stick"),
    path("update customer/<str:pk>/", views.updateCustomer, name="update_customer"),
    path(
        "update technician/<str:pk>/", views.updateTechnician, name="update_technician"
    ),
    # ::::::::::::::delete::::::::::::::
    path(
        "delete/<str:model_name>/<int:object_id>/",
        views.delete_object,
        name="delete_object",
    ),
    # ::::::::::::::PDF::::::::::::::
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
    # ::::::::::::::PRINT::::::::::::::
    path(
        "print-maintenance/<int:maintenance_id>/",
        views.print_maintenance_summary,
        name="print_maintenance",
    ),
    # ::::::::::::::customer-autocomplete::::::::::::::
    path(
        "customer-autocomplete/",
        views.CustomerAutocomplete.as_view(),
        name="customer-autocomplete",
    ),
    path("api/customer/<int:pk>/", views.get_customer_phone, name="get_customer_phone"),
]
