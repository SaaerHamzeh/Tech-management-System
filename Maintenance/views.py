from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import *
from .models import *
from .filters import *

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

# for deleting
from django.shortcuts import redirect, get_object_or_404

# from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.contrib import messages  # 👈 لإظهار الرسائل
from dal import autocomplete


def dashboard(request):
    maintenances = MaintenanceInfo.objects.all().order_by("-id")
    total_tasks = maintenances.count()
    total_cost_tasks = maintenances.aggregate(total=Sum("cost"))["total"]
    maintenances_rounded_total = round(total_cost_tasks, 0) if total_cost_tasks else 0
    total_pending_tasks = maintenances.filter(maintenance_status="Pending").count()
    total_In_Progress_tasks = maintenances.filter(
        maintenance_status="In Progress"
    ).count()
    total_Completed_tasks = maintenances.filter(maintenance_status="Completed").count()
    total_Cancelled_tasks = maintenances.filter(maintenance_status="Cancelled").count()
    # -------------------------------
    sales = Sales.objects.all().order_by("-id")
    total_sales = sales.count()

    total_price_sales = sales.aggregate(total=Sum("price"))["total"]
    sales_rounded_price = round(total_price_sales, 0) if total_price_sales else 0
    total_cost_sales = sales.aggregate(total=Sum("cost"))["total"]
    sales_rounded_total = round(total_cost_sales, 0) if total_cost_sales else 0
    net_sales = sales.aggregate(total=Sum("net"))["total"]
    sales_rounded_net_sales = round(net_sales, 0) if net_sales else 0

    # -------------------------------
    pc = PC.objects.all()
    laptops = Laptop.objects.all()
    playsations = PlayStation.objects.all()
    gamesticks = GameStick.objects.all()
    routers = Router.objects.all()
    payments = Payments.objects.all().order_by("-id")

    MaintenanceFilter = MaintenanceInfoFilter(request.GET, queryset=maintenances)
    maintenances = MaintenanceFilter.qs

    salesFilter = SalesFilter(request.GET, queryset=sales)
    sales = salesFilter.qs

    paymentsFilter = PaymentsFilter(request.GET, queryset=payments)
    payments = paymentsFilter.qs

    status_classes = {
        "Completed": "bg-success",
        "Pending": "bg-warning",
        "In Progress": "bg-info",
    }
    context = {
        "pc": pc,
        "maintenances": maintenances,
        "sales": sales,
        "payments": payments,
        "laptops": laptops,
        "playsations": playsations,
        "gamesticks": gamesticks,
        "routers": routers,
        "MaintenanceFilter": MaintenanceFilter,
        "salesFilter": salesFilter,
        "paymentsFilter": paymentsFilter,
        "total_tasks": total_tasks,
        "maintenances_rounded_total": maintenances_rounded_total,
        "total_pending_tasks": total_pending_tasks,
        "total_In_Progress_tasks": total_In_Progress_tasks,
        "total_Completed_tasks": total_Completed_tasks,
        "total_Cancelled_tasks": total_Cancelled_tasks,
        "total_sales": total_sales,
        "sales_rounded_price": sales_rounded_price,
        "sales_rounded_total": sales_rounded_total,
        "sales_rounded_net_sales": sales_rounded_net_sales,
        "status_classes": status_classes,
    }
    return render(request, "Maintenance/dashboard.html", context)


def devicesMaintenance(request):
    pc = PC.objects.all().order_by("-id")
    laptops = Laptop.objects.all().order_by("-id")
    playsations = PlayStation.objects.all().order_by("-id")
    gamesticks = GameStick.objects.all().order_by("-id")
    routers = Router.objects.all().order_by("-id")
    context = {
        "pc": pc,
        "laptops": laptops,
        "playsations": playsations,
        "gamesticks": gamesticks,
        "routers": routers,
    }
    return render(request, "Maintenance/devices_maintenance.html", context)


# ______________________________manage_maintenances_____________________________


def get_device_form(request):
    device_type = request.GET.get("type")

    form_classes = {
        "pc": PCForm,
        "laptop": LaptopForm,
        "playstation": PlaystationForm,
        "gamestick": GameStickForm,
        "router": RouterForm,
    }

    form_class = form_classes.get(device_type)
    if not form_class:
        return HttpResponse("<p style='color:red;'>نوع الجهاز غير معروف</p>")

    form = form_class()
    html = render_to_string("Maintenance/partials/device_form.html", {"form": form})
    return HttpResponse(html)


def maintenance_form(request):
    if request.method == "POST":
        print("🔧 [DEBUG] POST DATA:", request.POST)  # ✅ طباعة كل البيانات المرسلة

        maintenance_form = MaintenanceInfoForm(request.POST)
        customer_form = CustomerForm(request.POST)
        device_type = request.POST.get("device_type")

        # فورمات الأجهزة
        laptop_form = LaptopForm(request.POST)
        pc_form = PCForm(request.POST)
        playstation_form = PlaystationForm(request.POST)
        gamestick_form = GameStickForm(request.POST)
        router_form = RouterForm(request.POST)

        # اختيار الفورم الصحيح حسب نوع الجهاز
        device_form = {
            "laptop": laptop_form,
            "pc": pc_form,
            "playstation": playstation_form,
            "gamestick": gamestick_form,
            "router": router_form,
        }.get(device_type, None)

        if not (
            maintenance_form.is_valid()
            and customer_form.is_valid()
            and device_form
            and device_form.is_valid()
        ):
            print("❌ [ERROR] maintenance_form errors:", maintenance_form.errors)
            print("❌ [ERROR] customer_form errors:", customer_form.errors)
            if device_form:
                print(f"❌ [ERROR] {device_type}_form errors:", device_form.errors)
            messages.error(request, "⚠️ تأكد من صحة جميع الحقول.")
        else:
            # 👤 إما زبون موجود أو جديد
            existing_customer = customer_form.cleaned_data.get("existing_customer")
            new_name = customer_form.cleaned_data.get("new_name")
            new_phone = customer_form.cleaned_data.get("new_phone")

            if existing_customer:
                customer_instance = existing_customer
            elif new_name and new_phone:
                customer_instance, _ = Customer.objects.get_or_create(
                    name=new_name, defaults={"phone": new_phone}
                )
            else:
                messages.error(
                    request, "يرجى إدخال اسم ورقم الزبون أو اختيار زبون موجود."
                )
                return render(
                    request,
                    "Maintenance/create_maintenance_order.html",
                    {
                        "maintenance_form": maintenance_form,
                        "customer_form": customer_form,
                        "laptop_form": laptop_form,
                        "pc_form": pc_form,
                        "playstation_form": playstation_form,
                        "gamestick_form": gamestick_form,
                        "router_form": router_form,
                    },
                )

            # الجهاز
            print("✅ [DEBUG] device_form.cleaned_data:", device_form.cleaned_data)
            device_instance = device_form.save(commit=False)
            device_instance.customer = customer_instance
            device_instance.device_type = device_type
            device_instance.save()

            # بيانات الصيانة
            maintenance = maintenance_form.save(commit=False)
            maintenance.customer = customer_instance
            maintenance.device_type = device_type
            setattr(maintenance, device_type, device_instance)
            maintenance.save()

            messages.success(request, "✅ تم إنشاء طلب صيانة بنجاح")
            return redirect("print_maintenance", maintenance_id=maintenance.id)

    else:
        maintenance_form = MaintenanceInfoForm()
        customer_form = CustomerForm()
        laptop_form = LaptopForm()
        pc_form = PCForm()
        playstation_form = PlaystationForm()
        gamestick_form = GameStickForm()
        router_form = RouterForm()
        device_type = None  # 👍 هون لازم نحطها

    return render(
        request,
        "Maintenance/create_maintenance_order.html",
        {
            "maintenance_form": maintenance_form,
            "customer_form": customer_form,
            "laptop_form": laptop_form,
            "pc_form": pc_form,
            "playstation_form": playstation_form,
            "gamestick_form": gamestick_form,
            "router_form": router_form,
            "device_type": device_type,
        },
    )


def maintenance_form(request):
    device_type = request.POST.get("device_type") if request.method == "POST" else None

    # الأساسيات
    maintenance_form = MaintenanceInfoForm(request.POST or None)
    customer_form = CustomerForm(request.POST or None)
    laptop_form = LaptopForm(request.POST or None)
    pc_form = PCForm(request.POST or None)
    playstation_form = PlaystationForm(request.POST or None)
    gamestick_form = GameStickForm(request.POST or None)
    router_form = RouterForm(request.POST or None)

    # الفورمست حسب نوع الجهاز
    ram_formset = hard_formset = None
    if device_type == "pc":
        ram_formset = pcRAMFormSet(request.POST or None, prefix="ram")
        hard_formset = pcHardFormSet(request.POST or None, prefix="hard")
        device_form = pc_form
    elif device_type == "laptop":
        ram_formset = laptopRAMFormSet(request.POST or None, prefix="ram")
        hard_formset = laptopHardFormSet(request.POST or None, prefix="hard")
        device_form = laptop_form
    else:
        device_form = {
            "playstation": playstation_form,
            "gamestick": gamestick_form,
            "router": router_form,
        }.get(device_type)

    if request.method == "POST":
        if not (
            maintenance_form.is_valid()
            and customer_form.is_valid()
            and device_form
            and device_form.is_valid()
            and (ram_formset is None or ram_formset.is_valid())
            and (hard_formset is None or hard_formset.is_valid())
        ):
            messages.error(request, "⚠️ تأكد من صحة جميع الحقول.")
        else:
            existing_customer = customer_form.cleaned_data.get("existing_customer")
            new_name = customer_form.cleaned_data.get("new_name")
            new_phone = customer_form.cleaned_data.get("new_phone")

            if existing_customer:
                customer_instance = existing_customer
            elif new_name and new_phone:
                customer_instance, _ = Customer.objects.get_or_create(
                    name=new_name, defaults={"phone": new_phone}
                )
            else:
                messages.error(
                    request, "يرجى إدخال اسم ورقم الزبون أو اختيار زبون موجود."
                )
                return render(
                    request,
                    "Maintenance/create_maintenance_order.html",
                    {
                        "maintenance_form": maintenance_form,
                        "customer_form": customer_form,
                        "laptop_form": laptop_form,
                        "pc_form": pc_form,
                        "playstation_form": playstation_form,
                        "gamestick_form": gamestick_form,
                        "router_form": router_form,
                        "ram_formset": ram_formset,
                        "hard_formset": hard_formset,
                        "device_type": device_type,
                    },
                )

            # إنشاء الجهاز
            device_instance = device_form.save(commit=False)
            # ✨ طباعة لتتأكد إنو القيم وصلت
            print(f"[DEBUG] issue: {device_instance.issue}")
            print(f"[DEBUG] serial_number: {device_instance.serial_number}")

            device_instance.customer = customer_instance
            device_instance.device_type = device_type
            device_instance.save()

            # حفظ الرامات والهاردات إن وجدت
            if device_type in ["pc", "laptop"]:
                ram_formset.instance = device_instance
                ram_formset.save()
                hard_formset.instance = device_instance
                hard_formset.save()

            # إنشاء الصيانة
            maintenance = maintenance_form.save(commit=False)
            maintenance.customer = customer_instance
            maintenance.device_type = device_type
            setattr(maintenance, device_type, device_instance)
            maintenance.save()

            messages.success(request, "✅ تم إنشاء طلب صيانة بنجاح")
            return redirect("print_maintenance", maintenance_id=maintenance.id)

    # معالجة GET أو عرض الصفحة بعد فشل POST
    if not ram_formset and device_type == "pc":
        ram_formset = pcRAMFormSet(prefix="ram")
        hard_formset = pcHardFormSet(prefix="hard")
    elif not ram_formset and device_type == "laptop":
        ram_formset = laptopRAMFormSet(prefix="ram")
        hard_formset = laptopHardFormSet(prefix="hard")

    return render(
        request,
        "Maintenance/create_maintenance_order.html",
        {
            "maintenance_form": maintenance_form,
            "customer_form": customer_form,
            "laptop_form": laptop_form,
            "pc_form": pc_form,
            "playstation_form": playstation_form,
            "gamestick_form": gamestick_form,
            "router_form": router_form,
            "ram_formset": ram_formset,
            "hard_formset": hard_formset,
            "device_type": device_type,
        },
    )


def updateMaintenance(request, pk):
    maintenance_instance = get_object_or_404(MaintenanceInfo, id=pk)
    device_type = maintenance_instance.device_type
    existing_customer = maintenance_instance.customer
    device_instance = getattr(maintenance_instance, device_type)

    # فورمات الأجهزة
    laptop_form = LaptopForm(request.POST or None, instance=maintenance_instance.laptop)
    pc_form = PCForm(request.POST or None, instance=maintenance_instance.pc)
    playstation_form = PlaystationForm(
        request.POST or None, instance=maintenance_instance.playstation
    )
    gamestick_form = GameStickForm(
        request.POST or None, instance=maintenance_instance.gamestick
    )
    router_form = RouterForm(request.POST or None, instance=maintenance_instance.router)

    device_form = {
        "laptop": laptop_form,
        "pc": pc_form,
        "playstation": playstation_form,
        "gamestick": gamestick_form,
        "router": router_form,
    }.get(device_type)

    maintenance_form = MaintenanceInfoForm(
        request.POST or None, instance=maintenance_instance
    )

    customer_form = CustomerForm(
        request.POST or None,
        initial={
            "existing_customer": existing_customer,
            "new_name": "",
            "new_phone": existing_customer.phone if existing_customer else "",
        },
    )

    if request.method == "POST":
        if (
            maintenance_form.is_valid()
            and customer_form.is_valid()
            and device_form
            and device_form.is_valid()
        ):
            existing_customer = customer_form.cleaned_data.get("existing_customer")
            new_name = customer_form.cleaned_data.get("new_name")
            new_phone = customer_form.cleaned_data.get("new_phone")

            if existing_customer:
                customer_instance = existing_customer
            elif new_name and new_phone:
                customer_instance, _ = Customer.objects.get_or_create(
                    name=new_name, defaults={"phone": new_phone}
                )
            else:
                messages.error(request, "يرجى اختيار زبون أو إدخال بيانات زبون جديد.")
                return render(
                    request,
                    "Maintenance/create_maintenance_order.html",
                    {
                        "maintenance_form": maintenance_form,
                        "customer_form": customer_form,
                        "laptop_form": laptop_form,
                        "pc_form": pc_form,
                        "playstation_form": playstation_form,
                        "gamestick_form": gamestick_form,
                        "router_form": router_form,
                        "device_type": device_type,
                    },
                )

            # حفظ الجهاز
            device_instance = device_form.save(commit=False)
            device_instance.customer = customer_instance
            device_instance.device_type = device_type
            device_instance.save()

            # حفظ الصيانة
            maintenance = maintenance_form.save(commit=False)
            maintenance.customer = customer_instance
            setattr(maintenance, device_type, device_instance)
            maintenance.save()

            messages.success(request, "✅ تم تعديل طلب الصيانة بنجاح")
            return redirect("print_maintenance", maintenance_id=maintenance.id)

        else:
            messages.error(request, "⚠️ تأكد من صحة الحقول")

    return render(
        request,
        "Maintenance/create_maintenance_order.html",
        {
            "maintenance_form": maintenance_form,
            "customer_form": customer_form,
            "laptop_form": laptop_form,
            "pc_form": pc_form,
            "playstation_form": playstation_form,
            "gamestick_form": gamestick_form,
            "router_form": router_form,
            "device_type": device_type,
        },
    )


# ______________________________manage_sales_____________________________
def sales_form(request):
    if request.method == "POST":
        form = SalesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # قم بتوجيه المستخدم بعد الحفظ
    else:
        form = SalesForm()

    context = {"form": form}
    return render(request, "Maintenance/create_sale.html", context)


def updateSale(request, pk):
    sale = Sales.objects.get(id=pk)
    form = SalesForm(instance=sale)
    if request.method == "POST":
        form = SalesForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "form": form,
    }
    return render(request, "Maintenance/create_sale.html", context)


# ______________________________manage_payments_____________________________
def payments_form(request):
    if request.method == "POST":
        form = PaymentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")  # قم بتوجيه المستخدم بعد الحفظ
    else:
        form = PaymentsForm()

    context = {"form": form}
    return render(request, "Maintenance/create_payment.html", context)


def updatePayment(request, pk):
    payment = Payments.objects.get(id=pk)
    form = PaymentsForm(instance=payment)
    if request.method == "POST":
        form = PaymentsForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {
        "form": form,
    }
    return render(request, "Maintenance/create_payment.html", context)


# ______________________________manage_customers______________________________
def customers(request):
    customers = Customer.objects.all().order_by("-id")
    customersFilter = CustomerFilter(request.GET, queryset=customers)
    customers = customersFilter.qs
    context = {
        "customers": customers,
        "customersFilter": customersFilter,
    }
    return render(request, "Maintenance/customers.html", context)


def createCustomer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customers")

    context = {"form": form}
    return render(request, "Maintenance/create_customer.html", context)


def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customers")
    context = {
        "form": form,
    }
    return render(request, "Maintenance/create_customer.html", context)


# ______________________________manage_technicians______________________________
def technicians(request):
    technician = Technician.objects.all().order_by("-id")
    techniciansFilter = TechnicianFilter(request.GET, queryset=technician)
    technician = techniciansFilter.qs
    context = {
        "technicians": technician,
        "techniciansFilter": techniciansFilter,
    }
    return render(request, "Maintenance/technicians.html", context)


def createTechnician(request):
    form = TechnicianForm()
    if request.method == "POST":
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("technicians")

    context = {"form": form}
    return render(request, "Maintenance/create_technician.html", context)


def updateTechnician(request, pk):
    technician = Technician.objects.get(id=pk)
    form = TechnicianForm(instance=technician)
    if request.method == "POST":
        form = TechnicianForm(request.POST, instance=technician)
        if form.is_valid():
            form.save()
            return redirect("technicians")
    context = {
        "form": form,
    }
    return render(request, "Maintenance/create_technician.html", context)


# ______________________________manage_PCs______________________________
def createPC(request):
    pcform = PCForm()

    if request.method == "POST":
        pcform = PCForm(request.POST)
        ram_formset = pcRAMFormSet(request.POST, prefix="ram")
        hard_formset = pcHardFormSet(request.POST, prefix="hard")

        if pcform.is_valid() and ram_formset.is_valid() and hard_formset.is_valid():
            pc = pcform.save()
            # 💾 حفظ الرامات:
            ram_formset.instance = pc
            for ram_form in ram_formset:
                if ram_form.cleaned_data and not ram_form.cleaned_data.get(
                    "DELETE", False
                ):
                    ram = ram_form.save(commit=False)
                    ram.pc = pc
                    ram.save()

            # 💾 حفظ الهاردات:
            hard_formset.instance = pc
            for hard_form in hard_formset:
                if hard_form.cleaned_data and not hard_form.cleaned_data.get(
                    "DELETE", False
                ):
                    hard = hard_form.save(commit=False)
                    hard.pc = pc
                    hard.save()

            return redirect("devices")

    else:
        pcform = PCForm()
        ram_formset = pcRAMFormSet(queryset=pcRAM.objects.none(), prefix="ram")
        hard_formset = pcHardFormSet(queryset=pcHARD.objects.none(), prefix="hard")

    return render(
        request,
        "Maintenance/create_pc.html",
        {
            "pcform": pcform,
            "ram_formset": ram_formset,
            "hard_formset": hard_formset,
        },
    )


def updatePC(request, pk):
    pc = PC.objects.get(id=pk)

    pcform = PCForm(instance=pc)
    # formsets بالرغم من أنها موجودة، كانت غير مفعّلة في الكود
    ram_formset = pcRAMFormSet(queryset=pcRAM.objects.filter(pc=pc), prefix="ram")
    hard_formset = pcHardFormSet(queryset=pcHARD.objects.filter(pc=pc), prefix="hard")

    if request.method == "POST":
        pcform = PCForm(request.POST, instance=pc)
        ram_formset = pcRAMFormSet(
            request.POST, queryset=pcRAM.objects.filter(pc=pc), prefix="ram"
        )
        hard_formset = pcHardFormSet(
            request.POST,
            queryset=pcHARD.objects.filter(pc=pc),
            prefix="hard",
        )

        if pcform.is_valid() and ram_formset.is_valid() and hard_formset.is_valid():
            pc = pcform.save()

            # احفظ الرامات
            for ram_form in ram_formset:
                if ram_form.cleaned_data:
                    if ram_form.cleaned_data.get("DELETE", False):
                        if ram_form.instance.pk:
                            ram_form.instance.delete()
                    else:
                        ram = ram_form.save(commit=False)
                        ram.pc = pc
                        ram.save()

            # احفظ الهاردات
            for hard_form in hard_formset:
                if hard_form.cleaned_data:
                    if hard_form.cleaned_data.get("DELETE", False):
                        if hard_form.instance.pk:
                            hard_form.instance.delete()
                    else:
                        hard = hard_form.save(commit=False)
                        hard.pc = pc
                        hard.save()

            return redirect("devices")

    context = {
        "pcform": pcform,
        "ram_formset": ram_formset,
        "hard_formset": hard_formset,
    }

    return render(request, "Maintenance/create_pc.html", context)


def updatepcRAM(request, pk):

    ram = pcRAM.objects.get(id=pk)

    ramform = pcRAMForm(instance=ram)
    if request.method == "POST":

        ramform = pcRAMForm(request.POST, instance=ram)

        if ramform.is_valid():
            ramform.save()
            return redirect("devices")
    context = {
        "ramform": ramform,
    }
    return render(request, "Maintenance/update_pc_ram.html", context)


def updatepcHARD(request, pk):

    hard = pcHARD.objects.get(id=pk)

    hardform = pcHardForm(instance=hard)
    if request.method == "POST":

        hardform = pcHardForm(request.POST, instance=hard)

        if hardform.is_valid():
            hardform.save()
            return redirect("devices")
    context = {
        "hardform": hardform,
    }
    return render(request, "Maintenance/update_pc_hard.html", context)


# ______________________________manage_laptops______________________________
def createLaptop(request):
    laptopform = LaptopForm()

    if request.method == "POST":
        laptopform = LaptopForm(request.POST)
        ram_formset = laptopRAMFormSet(request.POST, prefix="ram")
        hard_formset = laptopHardFormSet(request.POST, prefix="hard")

        if laptopform.is_valid() and ram_formset.is_valid() and hard_formset.is_valid():
            laptop = laptopform.save()

            # 💾 حفظ الرامات:
            ram_formset.instance = laptop
            for ram_form in ram_formset:
                if ram_form.cleaned_data and not ram_form.cleaned_data.get(
                    "DELETE", False
                ):
                    ram = ram_form.save(commit=False)
                    ram.laptop = laptop
                    ram.save()

            # 💾 حفظ الهاردات:
            hard_formset.instance = laptop
            for hard_form in hard_formset:
                if hard_form.cleaned_data and not hard_form.cleaned_data.get(
                    "DELETE", False
                ):
                    hard = hard_form.save(commit=False)
                    hard.laptop = laptop
                    hard.save()

            return redirect("devices")  # ✅ عدّل حسب مشروعك
    else:
        laptopform = LaptopForm()
        ram_formset = laptopRAMFormSet(queryset=laptopRAM.objects.none(), prefix="ram")
        hard_formset = laptopHardFormSet(
            queryset=laptopHARD.objects.none(), prefix="hard"
        )

    return render(
        request,
        "Maintenance/create_laptop.html",
        {
            "laptopform": laptopform,
            "ram_formset": ram_formset,
            "hard_formset": hard_formset,
        },
    )


def updateLaptop(request, pk):
    laptop = Laptop.objects.get(id=pk)

    laptopform = LaptopForm(instance=laptop)

    # formsets بالرغم من أنها موجودة، كانت غير مفعّلة في الكود
    ram_formset = laptopRAMFormSet(
        queryset=laptopRAM.objects.filter(laptop=laptop), prefix="ram"
    )
    hard_formset = laptopHardFormSet(
        queryset=laptopHARD.objects.filter(laptop=laptop), prefix="hard"
    )

    if request.method == "POST":
        laptopform = LaptopForm(request.POST, instance=laptop)
        ram_formset = laptopRAMFormSet(
            request.POST, queryset=laptopRAM.objects.filter(laptop=laptop), prefix="ram"
        )
        hard_formset = laptopHardFormSet(
            request.POST,
            queryset=laptopHARD.objects.filter(laptop=laptop),
            prefix="hard",
        )

        if laptopform.is_valid() and ram_formset.is_valid() and hard_formset.is_valid():
            laptop = laptopform.save()

            # احفظ الرامات
            for ram_form in ram_formset:
                if ram_form.cleaned_data:
                    if ram_form.cleaned_data.get("DELETE", False):
                        if ram_form.instance.pk:
                            ram_form.instance.delete()
                    else:
                        ram = ram_form.save(commit=False)
                        ram.laptop = laptop
                        ram.save()

            # احفظ الهاردات
            for hard_form in hard_formset:
                if hard_form.cleaned_data:
                    if hard_form.cleaned_data.get("DELETE", False):
                        if hard_form.instance.pk:
                            hard_form.instance.delete()
                    else:
                        hard = hard_form.save(commit=False)
                        hard.laptop = laptop
                        hard.save()

            return redirect("devices")

    context = {
        "laptopform": laptopform,
        "ram_formset": ram_formset,
        "hard_formset": hard_formset,
    }

    return render(request, "Maintenance/create_laptop.html", context)


def updateLaptopRAM(request, pk):

    ram = laptopRAM.objects.get(id=pk)

    ramform = laptopRAMForm(instance=ram)
    if request.method == "POST":

        ramform = laptopRAMForm(request.POST, instance=ram)

        if ramform.is_valid():
            ramform.save()
            return redirect("devices")
    context = {
        "ramform": ramform,
    }
    return render(request, "Maintenance/update_lap_ram.html", context)


def updateLaptopHARD(request, pk):

    hard = laptopHARD.objects.get(id=pk)

    hardform = laptopHardForm(instance=hard)
    if request.method == "POST":

        hardform = laptopHardForm(request.POST, instance=hard)

        if hardform.is_valid():
            hardform.save()
            return redirect("devices")
    context = {
        "hardform": hardform,
    }
    return render(request, "Maintenance/update_lap_hard.html", context)


# ______________________________manage_playstations______________________________
def createPS(request):
    playstationform = PlaystationForm()

    if request.method == "POST":

        playstationform = PlaystationForm(request.POST)

        if playstationform.is_valid():
            playstationform.save()
            return redirect("devices")

    context = {
        "playstationform": playstationform,
    }
    return render(request, "Maintenance/create_ps.html", context)


def updatePS(request, pk):

    playstation = PlayStation.objects.get(id=pk)

    playstationform = PlaystationForm(instance=playstation)
    if request.method == "POST":

        playstationform = PlaystationForm(request.POST, instance=playstation)

        if playstationform.is_valid():
            playstationform.save()
            return redirect("devices")
    context = {
        "playstationform": playstationform,
    }
    return render(request, "Maintenance/create_ps.html", context)


# ______________________________manage_routers______________________________
def createRouter(request):
    routerform = RouterForm()

    if request.method == "POST":

        routerform = RouterForm(request.POST)

        if routerform.is_valid():
            routerform.save()
            return redirect("devices")

    context = {
        "routerform": routerform,
    }
    return render(request, "Maintenance/create_router.html", context)


def updateRouter(request, pk):

    router = Router.objects.get(id=pk)

    routerform = RouterForm(instance=router)
    if request.method == "POST":

        routerform = RouterForm(request.POST, instance=router)

        if routerform.is_valid():
            routerform.save()
            return redirect("devices")
    context = {
        "routerform": routerform,
    }
    return render(request, "Maintenance/create_router.html", context)


# ______________________________manage_gamesticks_____________________________
def createPsStick(request):
    gamestick_form = GameStickForm()

    if request.method == "POST":

        gamestick_form = GameStickForm(request.POST)

        if gamestick_form.is_valid():
            gamestick_form.save()
            return redirect("devices")

    context = {
        "gamestick_form": gamestick_form,
    }
    return render(request, "Maintenance/create_gamestick.html", context)


def updatePsStick(request, pk):

    gamestick = GameStick.objects.get(id=pk)

    gamestick_form = GameStickForm(instance=gamestick)
    if request.method == "POST":

        gamestick_form = GameStickForm(request.POST, instance=gamestick)

        if gamestick_form.is_valid():
            gamestick_form.save()
            return redirect("devices")
    context = {
        "gamestick_form": gamestick_form,
    }
    return render(request, "Maintenance/create_gamestick.html", context)


# ______________________________delete_view____________________________
def delete_object(request, model_name, object_id):
    model = apps.get_model("Maintenance", model_name)  # استبدل 'app_name' باسم تطبيقك
    obj = get_object_or_404(model, id=object_id)
    obj.delete()
    previous_page = request.META.get("HTTP_REFERER")
    if previous_page:
        return redirect(previous_page)
    else:
        return redirect("/")


# _____________________________generate_PDF_view____________________________


def generate_pdf(request):
    maintenances = MaintenanceInfo.objects.all()
    maintenance_filter = MaintenanceInfoFilter(request.GET, queryset=maintenances)
    filtered_maintenances = maintenance_filter.qs

    # إنشاء ملف HTML باستخدام البيانات المفلترة
    html_string = render_to_string(
        "Maintenance/maintenance_pdf.html", {"maintenances": filtered_maintenances}
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="maintenance_report.pdf"'
    HTML(string=html_string).write_pdf(response)

    return response


def print_maintenance_summary(request, maintenance_id):
    maintenance = get_object_or_404(MaintenanceInfo, id=maintenance_id)

    device = (
        maintenance.pc
        or maintenance.laptop
        or maintenance.playstation
        or maintenance.gamestick
        or maintenance.router
    )

    # تجهيز الحقول بشكل آمن
    device_fields = []
    if device:
        for field in device._meta.fields:
            if field.name != "id":
                value = getattr(device, field.name)
                device_fields.append(
                    {"label": field.verbose_name.title(), "value": value}
                )

    return render(
        request,
        "Maintenance/print_summary.html",
        {
            "maintenance": maintenance,
            "device_fields": device_fields,
        },
    )


# _____________________________autocomplete_customer___________________________
class CustomerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Customer.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def create_object(self, text):  # 👈 هذا ما يسمح بإنشاء زبون جديد
        return Customer.objects.create(name=text)


from django.http import JsonResponse


def get_customer_phone(request, pk):
    customer = Customer.objects.get(pk=pk)
    return JsonResponse({"phone": customer.phone})
