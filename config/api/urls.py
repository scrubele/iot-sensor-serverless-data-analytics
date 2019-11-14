from django.conf.urls import url, include
from rest_framework import routers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import SensorViewSet

router = routers.DefaultRouter()
router.register(r'sensors', SensorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]