from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from api.models import Sensor
from api.serializers import SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer 