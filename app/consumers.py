from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import action
from .serializers import *
from .services import *


class MyCons(GenericAsyncAPIConsumer):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    async def connect(self):
        self.key = self.scope.get("device", None)
        print(f"Connected {self.scope.get('client')}")
        if self.key:
            self.room_group_name = f'chat_{self.key}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            self.user = self.scope.get("user", None)
            await self.channel_layer.group_add(
                "chat_datas",
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
                "chat_datas",
                self.channel_name
            )

    @action()
    async def getdatas(self, keys, **kwargs):
        d = await getDevice_owner(self.user)
        f = [key for key in keys if key in d]

        for key in f:
            await self.send_json(
                {
                    "message": f"{key} data has been requested",
                })
            await self.channel_layer.group_send(f"chat_{key}", {
                "type": "typing_msg",
                "types": "getdatas"
            })

    @action()
    async def getcontrolling(self, **kwargs):
        await self.send_json({"type": "controlling", "controlling": self.key.controlling})

    @action()
    async def setcontrolling(self, controlling, keys, **kwargs):
        d = await getDevice_owner(self.user)
        f = [key for key in keys if key in d]

        for key in f:
            await self.send_json(
                {
                    "message": f"Control was send {key}",
                    "controlling": await set_device_controlling(key, controlling)
                })

            await self.channel_layer.group_send(f"chat_{key}", {
                "type": "controlling_msg",
                "controlling": controlling
            })

    @action()
    async def setdatas(self, datas, **kwargs):
        await set_device_datas(self.key, datas)

        await self.channel_layer.group_send("chat_datas", {
            "type": "data_msg",
            "datas": datas,
            "key": self.key
        })

    async def data_msg(self, event):
        datas = event["datas"]
        key = event["key"]
        await self.send_json({
            "type": "data",
            "datas": datas,
            "key": str(key)
        })

    async def controlling_msg(self, event):
        controlling = event["controlling"]
        print(controlling)
        await self.send_json({
            "type": "controlling",
            "controlling": controlling
        })

    async def typing_msg(self, event):
        types = event["types"]

        await self.send_json({
            "type": types
        })
