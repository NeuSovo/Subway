# Generated by Django 2.1.7 on 2019-03-02 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0008_auto_20190301_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.CharField(max_length=155, verbose_name='设备名称'),
        ),
    ]
