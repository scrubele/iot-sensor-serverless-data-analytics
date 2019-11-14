from django.contrib import admin
from api.models import Sensor
# Register your models here.
@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id','name','sensor_type','date','time','lat','lng','measurement_value')