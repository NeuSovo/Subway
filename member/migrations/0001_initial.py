# Generated by Django 2.1.3 on 2018-11-10 06:17

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
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=120, verbose_name='部门名称')),
                ('dept_boss', models.CharField(max_length=30, verbose_name='负责人')),
                ('dept_position', models.CharField(max_length=10, verbose_name='职务')),
                ('boos_phone', models.CharField(max_length=11, verbose_name='联系电话')),
            ],
            options={
                'verbose_name': '部门',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=20)),
                ('enp', models.CharField(max_length=155)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_dept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Departments')),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
            },
        ),
    ]