from channels.db import database_sync_to_async
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
