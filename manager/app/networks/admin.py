from django.contrib import admin
from .models import Switch, Vlan

# Register your models here.
admin.site.register(Switch)
admin.site.register(Vlan)