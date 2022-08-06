import json
from channels.db import database_sync_to_async
from api.models import User
from app.models import Device


@database_sync_to_async
def set_device_datas(key, datas):
    key.datas = datas
    key.save()
    return datas


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
    return Device.objects.get(key=key, owner=owner).controlling