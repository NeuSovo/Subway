# Generated by Django 2.1.3 on 2019-01-11 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20190111_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='sex',
            field=models.CharField(choices=[('男', '男'), ('女', '女')], default=' ', max_length=5, verbose_name='性别'),
        ),
    ]