# Generated by Django 2.1.3 on 2019-01-09 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20190109_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignaccount',
            name='id',
        ),
        migrations.AlterField(
            model_name='assignaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
