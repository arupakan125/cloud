from django.shortcuts import render
from rest_framework import viewsets
from .models import Network, Vlan
from .serializers import NetworkSerializer, VlanSerializer

# Create your views here.
class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class VlanViewSet(viewsets.ModelViewSet):
    queryset = Vlan.objects.all()
    serializer_class = VlanSerializer