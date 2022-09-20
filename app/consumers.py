import dataclasses
from json import JSONDecodeError
from djangochannelsrestframework.generics import AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import action
from .serializers import *
from .services import *


class MyCons(AsyncAPIConsumer):

    async def connect(self):
        self.key: Device = self.scope.get("device", None)
        print(f"Connected {self.scope.get('client')}")

        self.user = self.scope.get("user", None)
        self.datachat_name = f"datachat_{self.scope.get('user_token')}"
        print("Datachat", self.datachat_name)

        if self.key:
            self.room_group_name = f'chat_{self.key}'
            print(self.room_group_name)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            await self.channel_layer.group_add(
                self.datachat_name,
                self.channel_name
            )
        await self.accept()

    async def disconnect(self, code):
        print(f"DISCONNECT {self.scope.get('client')}")
        if self.key:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        else:
            await self.channel_layer.group_discard(
                self.datachat_name,
                self.channel_name
            )
    # async def receive(self, text_data=None, bytes_data=None, **kwargs):
    #     print(text_data)

    @action()
    async def setMainMoonSuitParameter(self, **kwargs):
        if not self.key:
            return await self.send_json({"success": False, "message": "You logged in as client"})
        
        # param = MoonSuitParametr(**kwargs)
        kwargs.pop("action")
        kwargs.pop("request_id")
        await set_moonsuit_parameter(kwargs, device=self.key)
        
        await self.channel_layer.group_send(self.datachat_name, {
            "type": "data_msg",
            "datas": kwargs,
            "key": str(self.key)
        })

    
    @action()
    async def getMainMoonsuitParameter(self, key, **kwargs):
        await self.send_json(
            {
                "message": f"{key} data has been requested",
            })
        await self.channel_layer.group_send(f"chat_{key}", {
            "type": "typing_msg",
            "types": "getdatas"
        })

    @action()
    async def getMainMoonsuitParameterDB(self, **kwargs):
        key = kwargs.get("key", None)
        if self.key:
            key = self.key
        await self.send_json({"type": "data", "datas": await getMoonSuitData(key)})

    @action()
    async def getcontrolling(self, **kwargs):
        if not self.key:
            return await self.send_json({"success": False, "message": "You logged in as client"})
        await self.send_json({"type": "controlling", "controlling": self.key.controlling})

    @action()
    async def setcontrolling(self, controlling, keys, **kwargs):
        d = await getDevice_owner(self.user)
        f = [key for key in keys if key in d]

        for key in f:
            print(key)
            await self.send_json(
                {
                    "message": f"Control was send {key}",
                    "controlling": await set_device_controlling(key, controlling)
                })

            await self.channel_layer.group_send(f"chat_{key}", {
                "type": "controlling_msg",
                "controlling": controlling
            })

    async def controlling_msg(self, event):
        controlling = event["controlling"]
        await self.send_json({
            "type": "controlling",
            "controlling": controlling
        })

    async def typing_msg(self, event):
        types = event["types"]

        await self.send_json({
            "type": types
        })

    async def data_msg(self, event):
        datas = event["datas"]
        key = event["key"]
        await self.send_json({
            "type": "data",
            "datas": datas,
            "key": str(key)
        })
