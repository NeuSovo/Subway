# Generated by Django 2.1.7 on 2019-03-06 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0009_auto_20190302_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=20, verbose_name='设备名称'),
        ),
        migrations.AlterField(
            model_name='profess',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
