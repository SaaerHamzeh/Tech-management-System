from django.contrib import admin
from .models import *

# from .models import Customer

# Register your models here.
admin.site.register(Customer)
admin.site.register(Technician)
admin.site.register(MaintenanceInfo)
admin.site.register(Sales)
admin.site.register(Payments)
admin.site.register(PC)
admin.site.register(Laptop)
admin.site.register(laptopRAM)
admin.site.register(laptopHARD)
admin.site.register(pcRAM)
admin.site.register(pcHARD)
admin.site.register(PlayStation)
admin.site.register(Router)
admin.site.register(GameStick)

admin.site.register(News)
