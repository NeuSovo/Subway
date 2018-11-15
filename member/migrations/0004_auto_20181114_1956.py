# Generated by Django 2.1.3 on 2018-11-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='blood_type',
            field=models.CharField(max_length=10, null=True, verbose_name='血型'),
        ),
        migrations.AddField(
            model_name='member',
            name='nation',
            field=models.CharField(max_length=10, null=True, verbose_name='民族'),
        ),
        migrations.AlterField(
            model_name='member',
            name='birthday',
            field=models.CharField(max_length=50, null=True, verbose_name='出生年月'),
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=11, null=True, verbose_name='联系方式'),
        ),
        migrations.AlterField(
            model_name='member',
            name='position',
            field=models.CharField(max_length=50, null=True, verbose_name='职位'),
        ),
        migrations.AlterField(
            model_name='member',
            name='sex',
            field=models.CharField(max_length=5, null=True, verbose_name='性别'),
        ),
    ]