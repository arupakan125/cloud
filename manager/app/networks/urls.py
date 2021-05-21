from rest_framework import routers
from networks.views import NetworkViewSet, VlanViewSet

router = routers.DefaultRouter()
router.register(r'switchs', NetworkViewSet)
router.register(r'vlans', VlanViewSet)