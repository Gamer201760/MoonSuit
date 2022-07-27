# Generated by Django 4.0.6 on 2022-07-27 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('datas', models.JSONField(default={'hello': 'World'})),
                ('controlling', models.JSONField(default={'hello': 'World'})),
                ('key', models.UUIDField(default=uuid.UUID('9559d368-c633-4bdf-974b-f83ae6db6036'), primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=15)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
