# Generated by Django 2.1.7 on 2019-03-01 12:45

import core.utils
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0007_auto_20190228_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicetestinfo',
            name='device',
            field=core.utils.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='test', serialize=False, to='device.Device'),
        ),
    ]