import uuid
from django.db import models
from api.models import *


class Device(models.Model):
    name = models.CharField(max_length=30)
    controlling = models.JSONField(default=dict({"hello": "World"}))
    
    x = models.IntegerField(null=True, blank=True)
    y = models.IntegerField(null=True, blank=True)
    z = models.IntegerField(null=True, blank=True)
    
    bpm = models.IntegerField(null=True, blank=True)
    vibration = models.IntegerField(null=True, blank=True)
    bodytemp = models.FloatField(null=True, blank=True)

    #in suit
    tempin = models.FloatField(null=True, blank=True)
    humin = models.IntegerField(null=True, blank=True)
    pressurein = models.IntegerField(null=True, blank=True)
    #out suit
    tempout = models.FloatField(null=True, blank=True)
    pressureout = models.IntegerField(null=True, blank=True)

    tempcontrol = models.IntegerField(null=True, blank=True)

    #Air system
    co = models.FloatField(null=True, blank=True)
    o = models.FloatField(null=True, blank=True)
    pressureinairsys = models.FloatField(null=True, blank=True)
    speedflowair = models.FloatField(null=True, blank=True)
    #Cooling system
    tempbefore = models.FloatField(null=True, blank=True)
    tempafter = models.FloatField(null=True, blank=True)
    speedflowcooling = models.FloatField(null=True, blank=True) 

    #Voltage
    voltage = models.FloatField(null=True, blank=True)
    current = models.FloatField(null=True, blank=True)


    key = models.UUIDField(default=uuid.uuid4, primary_key=True)
    tag = models.CharField(max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.key)


