from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Technician(models.Model):
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(max_length=150, null=True)
    phone = models.CharField(max_length=150, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name if self.name else "Technician (No Name)"


class Device(models.Model):
    DEVICE_TYPES = [
        ("", "Pick a Device"),
        ("laptop", "Laptop"),
        ("pc", "PC"),
        ("playstation", "PlayStation"),
        ("gamestick", "GameStick"),
        ("router", "Router"),
    ]
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)

    class Meta:
        abstract = True  # لا يتم إنشاء جدول لهذا النموذج


class PC(models.Model):
    customer = models.CharField(max_length=100, null=True, blank=True)
    # customer_phone_number = models.CharField(max_length=15, null=True, blank=True)
    device_type_model = models.CharField(max_length=100, null=True, blank=True)
    issue = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    motherboard = models.CharField(max_length=100, null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)
    # primary_hard_drive = models.CharField(max_length=100, null=True, blank=True)
    secondary_hard_drive = models.CharField(max_length=100, null=True, blank=True)
    # ram = models.CharField(max_length=100, null=True, blank=True)
    igc = models.CharField(
        max_length=100, null=True, blank=True
    )  # Integrated Graphics Card
    dsgc = models.CharField(
        max_length=100, null=True, blank=True
    )  # Dedicated Graphics Card
    drive = models.CharField(
        max_length=100, null=True, blank=True
    )  # Optical Drive or other drives
    powersupply = models.CharField(max_length=100, null=True, blank=True)
    case_type = models.CharField(
        max_length=100, null=True, blank=True
    )  # نوع الهيكل (Tower, Desktop, etc.)
    cooling_system = models.CharField(
        max_length=100, null=True, blank=True
    )  # نظام التبريد
    expansion_slots = models.CharField(
        max_length=100, null=True, blank=True
    )  # فتحات التوسعة
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device_type_model}-{self.serial_number}"


class pcRAM(models.Model):
    pc = models.ForeignKey(
        PC, null=True, blank=True, related_name="rams", on_delete=models.CASCADE
    )
    ram_type = models.CharField(max_length=50, null=True, blank=True)
    ram_size = models.CharField(max_length=50, null=True, blank=True)
    ram_serial_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.pc}-{self.ram_type}-{self.ram_size}"


class pcHARD(models.Model):
    pc = models.ForeignKey(
        PC, null=True, blank=True, related_name="hards", on_delete=models.CASCADE
    )
    hard_type = models.CharField(
        max_length=50, null=True, blank=True, choices=[("SSD", "SSD"), ("HDD", "HDD")]
    )
    hard_size = models.CharField(max_length=50, null=True, blank=True)
    hard_serial_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.pc}-{self.hard_type}-{self.hard_size}"


class Laptop(models.Model):
    customer = models.CharField(max_length=100, null=True, blank=True)
    # customer_phone_number = models.CharField(max_length=15, null=True, blank=True)
    device_type_model = models.CharField(max_length=100, null=True, blank=True)
    issue = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    processor = models.CharField(max_length=100, null=True, blank=True)

    secondary_hard_drive = models.CharField(max_length=100, null=True, blank=True)

    igc = models.CharField(max_length=100, null=True, blank=True)
    dsgc = models.CharField(max_length=100, null=True, blank=True)
    drive = models.CharField(max_length=100, null=True, blank=True)
    powersupply = models.CharField(max_length=100, null=True, blank=True)
    monitor_serial_number = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device_type_model}-{self.serial_number}"


class laptopRAM(models.Model):
    laptop = models.ForeignKey(
        Laptop, null=True, blank=True, related_name="rams", on_delete=models.CASCADE
    )
    ram_type = models.CharField(max_length=50, null=True, blank=True)
    ram_size = models.CharField(max_length=50, null=True, blank=True)
    ram_serial_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.laptop}-{self.ram_type}-{self.ram_size}"


class laptopHARD(models.Model):
    laptop = models.ForeignKey(
        Laptop, null=True, blank=True, related_name="hards", on_delete=models.CASCADE
    )
    hard_type = models.CharField(
        max_length=50, null=True, blank=True, choices=[("SSD", "SSD"), ("HDD", "HDD")]
    )
    hard_size = models.CharField(max_length=50, null=True, blank=True)
    hard_serial_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.laptop}-{self.hard_type}-{self.hard_size}"


class PlayStation(models.Model):
    customer = models.CharField(max_length=100, null=True, blank=True)
    # customer_phone_number = models.CharField(max_length=15, null=True, blank=True)
    device_type_model = models.CharField(
        max_length=100,
        choices=[
            ("PS2", "PS2"),
            ("PS2 Slim", "PS2 Slim"),
            ("PS3", "PS3"),
            ("PS3 Slim", "PS3 Slim"),
            ("PS3 Super Slim", "PS3 Super Slim"),
            ("PS4", "PS4"),
            ("PS4 Slim", "PS4 Slim"),
            ("PS4 Pro", "PS4 Pro"),
            ("PS5", "PS5"),
            ("PS5 Digital Edition", "PS5 Digital Edition"),
        ],
        blank=True,
        null=True,
    )
    issue = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    storage = models.CharField(max_length=100, null=True, blank=True)
    power_supply = models.CharField(max_length=100, null=True, blank=True)
    firmware_version = models.CharField(max_length=100, null=True, blank=True)
    accessories = models.TextField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.device_type_model}-{self.serial_number}"


class GameStick(models.Model):

    customer = models.CharField(max_length=100, null=True, blank=True)
    # customer_phone_number = models.CharField(max_length=15, null=True, blank=True)

    model = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )

    type = models.CharField(
        max_length=150,
        choices=[
            ("Orginal", "Orginal"),
            ("copy", "copy"),
        ],
        null=True,
        blank=True,
    )
    stick_number = models.IntegerField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("NEW", "NEW"),
            ("USED", "USED"),
            ("OTHER", "OTHER"),
        ],
    )
    issue = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.model}-{self.type}"


class Router(models.Model):
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer = models.CharField(max_length=100, null=True, blank=True)
    # customer_phone_number = models.CharField(max_length=15, null=True, blank=True)
    # Basic information
    brand = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    model = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    serial_number = models.CharField(max_length=100, blank=True, null=True, unique=True)
    mac_address = models.CharField(
        max_length=17, unique=True, blank=True, null=True
    )  # MAC address format: XX:XX:XX:XX:XX:XX

    # Status of the router
    status = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[
            ("NEW", "NEW"),
            ("USED", "USED"),
            ("OTHER", "OTHER"),
        ],
    )
    issue = models.CharField(max_length=20, null=True, blank=True)
    # Additional notes
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.serial_number})"


class MaintenanceInfo(models.Model):
    device_type = models.CharField(
        max_length=20,
        choices=Device.DEVICE_TYPES,
        null=True,
        blank=True,
    )
    pc = models.ForeignKey(PC, null=True, blank=True, on_delete=models.SET_NULL)
    laptop = models.ForeignKey(Laptop, null=True, blank=True, on_delete=models.SET_NULL)
    playstation = models.ForeignKey(
        PlayStation, null=True, blank=True, on_delete=models.SET_NULL
    )
    gamestick = models.ForeignKey(
        GameStick, null=True, blank=True, on_delete=models.SET_NULL
    )
    router = models.ForeignKey(Router, null=True, blank=True, on_delete=models.SET_NULL)

    customer = models.ForeignKey(
        Customer, null=True, blank=True, on_delete=models.SET_NULL
    )
    customer_phone_number = models.CharField(max_length=15, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.customer and not self.customer_phone_number:
            self.customer_phone_number = self.customer.phone
        super().save(*args, **kwargs)

    # Issue and maintenance details
    issue = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    maintenance_time = models.CharField(max_length=25, null=True, blank=True)
    maintenance_number = models.CharField(
        max_length=50, unique=True, null=True, blank=True
    )

    # Maintenance report and status
    maintenance_report = models.TextField(null=True, blank=True)
    maintenance_status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",
        null=True,
        blank=True,
    )

    technician_name = models.ForeignKey(
        Technician, null=True, blank=True, on_delete=models.SET_NULL
    )
    # Cost and handover details
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    handover_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.maintenance_number:
            now = timezone.now()
            timestamp = now.strftime("%Y%m%d%H%M%S")
            unique_id = str(MaintenanceInfo.objects.count() + 1).zfill(
                4
            )  # e.g., '0001'
            self.maintenance_number = f"{timestamp}-{unique_id}"
        super().save(*args, **kwargs)


class Sales(models.Model):
    item = models.CharField(max_length=100, verbose_name="Item", null=True, blank=True)
    model = models.CharField(
        max_length=100, verbose_name="Model", null=True, blank=True
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity", null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price", null=True, blank=True
    )
    received_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Received Amount",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Status",
        null=True,
        blank=True,
        choices=[
            ("NEW", "NEW"),
            ("USED", "USED"),
            ("OTHER", "OTHER"),
        ],
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    warranty = models.CharField(
        max_length=100, verbose_name="Warranty", null=True, blank=True
    )
    serial_number = models.CharField(
        max_length=100, verbose_name="Serial Number", null=True, blank=True
    )

    notes = models.TextField(verbose_name="Notes", null=True, blank=True)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Cost", null=True, blank=True
    )
    net = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Net", null=True, blank=True
    )

    description = models.TextField(verbose_name="Description", null=True, blank=True)

    def __str__(self):
        return f"{self.item} - {self.customer} - {self.serial_number}"


class Payments(models.Model):
    item = models.CharField(max_length=100, verbose_name="Item", null=True, blank=True)
    model = models.CharField(
        max_length=100, verbose_name="Model", null=True, blank=True
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity", null=True, blank=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price", null=True, blank=True
    )

    status = models.CharField(
        max_length=50,
        verbose_name="Status",
        null=True,
        blank=True,
        choices=[
            ("NEW", "NEW"),
            ("USED", "USED"),
            ("OTHER", "OTHER"),
        ],
    )

    warranty = models.CharField(
        max_length=100, verbose_name="Warranty", null=True, blank=True
    )
    serial_number = models.CharField(
        max_length=100, verbose_name="Serial Number", null=True, blank=True
    )

    notes = models.TextField(verbose_name="Notes", null=True, blank=True)

    description = models.TextField(verbose_name="Description", null=True, blank=True)

    source = models.CharField(
        max_length=100, verbose_name="Source", null=True, blank=True
    )

    def __str__(self):
        return f"{self.item} - {self.model} - {self.price}"


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


class News(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
