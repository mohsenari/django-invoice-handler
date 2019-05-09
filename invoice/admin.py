from django.contrib import admin

from .models import Invoice
from .models import Client
from .models import Doctor
from .models import Appointment
# Register your models here.

admin.site.register(Invoice)
admin.site.register(Client)
admin.site.register(Doctor)
admin.site.register(Appointment)
