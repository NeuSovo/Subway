# Generated by Django 2.0.6 on 2019-03-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='text',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='设置类别显示'),
        ),
    ]
