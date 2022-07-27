from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import action
from .serializers import *
from .services import *


class MyCons(GenericAsyncAPIConsumer):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    async def connect(self):
        key = self.scope.get("key", None)
        print(key)
        if key:
            self.room_group_name = f'chat_{key}'
                
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(self.room_group_name)
        else:
            await self.channel_layer.group_add(
                    "chat_datas",
                    self.channel_name
                )
        await self.accept()

    async def disconnect(self, code):
        print("DISCONNECT")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_discard(
            "chat_datas",
            self.channel_name
        )

    @action()
    async def getdatas(self, keys, **kwargs):
        for key in keys:
            print(key)
            await self.channel_layer.group_send(f"chat_{key}", {
                "type": "typing_msg",
                "types": "getdatas"
            })
            

    @action()
    async def setcontrolling(self, controlling, keys, **kwargs):

        for key in keys:
            await self.send_json(await set_device_controlling(key, controlling))
            await self.channel_layer.group_send(f"chat_{key}", {
                "type": "controlling_msg",
                "controlling": controlling
            })
    
    @action()
    async def setdatas(self, datas, **kwargs):
        key = self.scope["key"]
        print(key)
        await self.send_json(await set_device_datas(key, datas))

        await self.channel_layer.group_send("chat_datas", {
            "type": "data_msg",
            "datas": datas,
            "key": key
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