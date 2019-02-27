# Generated by Django 2.1.5 on 2019-02-27 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0005_auto_20190227_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='acceptor',
        ),
        migrations.AddField(
            model_name='devicetestinfo',
            name='acceptor',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='验收人'),
        ),
    ]