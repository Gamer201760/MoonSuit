# Generated by Django 4.0.6 on 2022-09-16 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='consumption',
            new_name='current',
        ),
    ]
