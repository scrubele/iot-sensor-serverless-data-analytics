import requests
import sched, time
import datetime
from random import random
import threading
import time

url = 'https://cloud-course-p5guh5uvlq-uc.a.run.app/api/sensors/'

class Sensor:
    def __init__(self, url, name, sensor_type, date="", time="", lat="", lng="", measurement_value=0):
        self.url = url
        self.name = name
        self.sensor_type = sensor_type
        self.date=datetime.datetime.now().date()
        self.time=datetime.datetime.now()
        self.lng=lng
        self.lat =lat
        self.measurement_valuкe=measurement_value

    def post_data(self, url):
        x = requests.post(url, data = self.__dict__)
        print(x.text)

def post_data_loop(sensor, time_sleep, max_value):
    starttime=time.time()
    print("started")
    while True:
        print(sensor.name)
        sensor.measurement_value = random()*100
        sensor.post_data(url)
        time.sleep(time_sleep - ((time.time() - starttime) % time_sleep))

if __name__=='__main__':
    humidity_sensor=Sensor(url="", name="humidity_1",sensor_type="humidity")
    temperature_sensor = Sensor(url="", name="temperature", sensor_type="temperature")
    lighting_sensor = Sensor(url="",name="lighting", sensor_type="lighting", lat=48.5, lng=49.7)
    
    humidity_thread = threading.Thread(name='humidity_sensor', target=post_data_loop, args=(humidity_sensor, 1, 100)) 
    tempeature_thread = threading.Thread(name='temperature_sensor', target=post_data_loop, args=(temperature_sensor, 1.2, 35))
    lighting_thread = threading.Thread(name='lighting_sensor', target=post_data_loop, args=(lighting_sensor, 1.3, 1000))
    
    humidity_thread.start()
    tempeature_thread.start()
    lighting_thread.start()  