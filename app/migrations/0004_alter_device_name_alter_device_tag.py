# Generated by Django 4.0.6 on 2022-07-29 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_device_key_alter_device_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='device',
            name='tag',
            field=models.CharField(max_length=15),
        ),
    ]