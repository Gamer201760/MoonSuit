from django.contrib import admin
from .models import *


# Register your models here.

class DeviceModel(admin.ModelAdmin):
    list_display = ("name", "owner", "key", "controlling")
    list_display_links = ("name", "owner", "key", "controlling")

admin.site.register(Device, DeviceModel)