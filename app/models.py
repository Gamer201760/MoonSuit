import uuid
from django.db import models
from api.models import *


class Device(models.Model):
    name = models.CharField(max_length=30)
    datas = models.JSONField(default={"hello": "World"})
    controlling = models.JSONField(default={"hello": "World"})
    key = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    tag = models.CharField(max_length=15)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.key)


