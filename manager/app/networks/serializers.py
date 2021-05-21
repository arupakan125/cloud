from rest_framework import serializers

from .models import Network, Vlan


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = ('id', 'name', 'created_at', 'updated_at')


class VlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlan
        fields = ('id', 'vlan', 'created_at', 'updated_at')