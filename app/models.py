import uuid
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Device(models.Model):
    name = models.CharField(max_length=30)
    datas = models.JSONField(blank=True)
    controlling = models.JSONField(blank=True)
    key = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    tag = models.CharField(max_length=15)

    def __str__(self) -> str:
        return str(self.key)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
