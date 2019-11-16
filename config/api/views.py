from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import Sensor
from api.serializers import SensorSerializer
from django.http import Http404 
from api.pub_sub import publish_message
import json
import datetime
import os

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer 

    def list(self, request):
        queryset = Sensor.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = SensorSerializer(queryset, many=True, context=serializer_context)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.headers['token'])
        if (request.headers['token'] !=
            os.getenv('PUBSUB_VERIFICATION_TOKEN')):
            return Response('Invalid request')

        print(request.data)
        serializer_context = {
            'request': request,
        }
        
        sensor_serializer = SensorSerializer(data=request.data, context=serializer_context)
        
        if sensor_serializer.is_valid():
            pass
            sensor = sensor_serializer.save()
        sensor_data = sensor_serializer.data
        try:
            sensor_data.pop('url')
        except:
            pass
        sensor_data = json.dumps(dict(sensor_data))
        print(sensor_data)
        publish_message(sensor_data)
        return  Response(sensor_serializer.data)


    