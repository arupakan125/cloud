from django.shortcuts import render
from rest_framework import viewsets
from .models import Switch, Vlan
from .serializers import SwitchSerializer, VlanSerializer

# Create your views here.
class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Switch.objects.all()
    serializer_class = SwitchSerializer


class VlanViewSet(viewsets.ModelViewSet):
    queryset = Vlan.objects.all()
    serializer_class = VlanSerializer