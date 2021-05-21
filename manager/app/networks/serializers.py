from rest_framework import serializers

from .models import Switch, Vlan


class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = ('id', 'name', 'created_at', 'updated_at')


class VlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlan
        fields = ('id', 'vlan', 'switch', 'created_at', 'updated_at')