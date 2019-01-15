# Generated by Django 2.1.3 on 2019-01-14 11:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=155, verbose_name='名称')),
                ('type_id', models.CharField(max_length=20, verbose_name='型号')),
                ('num', models.IntegerField(default=0, verbose_name='数量')),
                ('unit', models.CharField(max_length=10, verbose_name='单位')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=0, verbose_name='数量')),
                ('operation_date', models.DateTimeField(auto_now_add=True, verbose_name='操作日期')),
                ('operation_type', models.IntegerField(choices=[(0, 'in'), (1, 'out')], default=0, verbose_name='操作类型')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='material.Material')),
            ],
        ),
    ]
