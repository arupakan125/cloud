from django.contrib import admin
from .models import Network, Vlan

# Register your models here.
admin.site.register(Network)
admin.site.register(Vlan)