from channels.db import database_sync_to_async
from api.models import User
from app.models import Device
from .serializers import DeviceSerializer    

@database_sync_to_async
def set_device_controlling(key, controlling):
    key = Device.objects.get(key=key)
    key.controlling = controlling
    key.save()
    return controlling

@database_sync_to_async
def getDevice_owner(user: User) -> list:
    dcount = Device.objects.filter(owner=user).all()
    return [str(s.key) for s in dcount]

@database_sync_to_async
def get_device_controlling(key, owner):
    """
    Возвращает столбец "controlling" у устройства
    """
    return key.controlling


@database_sync_to_async
def set_moonsuit_parameter(parametr, device: Device):

    device.bpm = parametr.get("bpm", device.bpm)
    device.vibration = parametr.get("vibration", device.vibration)
    device.bodytemp = parametr.get("bodytemp", device.bodytemp)
    
    device.tempin = parametr.get("tempin", device.tempin)
    device.humin = parametr.get("humin", device.humin)
    device.pressurein = parametr.get("pressurein", device.pressurein)
    
    device.tempout = parametr.get("tempout", device.tempout)
    device.pressureout = parametr.get("pressureout", device.pressureout)
    
    device.tempcontrol = parametr.get("tempcontrol", device.tempcontrol)
    
    device.co = parametr.get("co", device.co)
    device.o = parametr.get("o", device.o)
    device.pressureinairsys = parametr.get("pressureinairsys", device.pressureinairsys)
    device.speedflowair = parametr.get("speedflowair", device.speedflowair)

    device.tempbefore = parametr.get("tempbefore", device.tempbefore)
    device.tempafter = parametr.get("tempafter", device.tempafter)
    device.speedflowcooling = parametr.get("speedflowcooling", device.speedflowcooling)

    device.voltage = parametr.get("voltage", device.voltage)
    device.current = parametr.get("current", device.current)

    device.save()

@database_sync_to_async
def getMoonSuitData(key):
    print(type(key))
    if type(key) == "str":
        key = Device.objects.get(key=key)
    return DeviceSerializer(key).data