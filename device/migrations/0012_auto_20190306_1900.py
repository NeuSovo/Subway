# Generated by Django 2.1.7 on 2019-03-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0011_auto_20190306_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='t3',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='取样时间'),
        ),
        migrations.AlterField(
            model_name='device',
            name='z6',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='进场时间'),
        ),
    ]
