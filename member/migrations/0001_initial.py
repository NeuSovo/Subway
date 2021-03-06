# Generated by Django 2.1.3 on 2019-01-11 08:56


import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('position', models.CharField(blank=True, max_length=20, null=True, verbose_name='职位')),
                ('enp', models.CharField(blank=True, max_length=155, null=True, verbose_name='密码')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=120, unique=True, verbose_name='部门名称')),
                ('dept_boss', models.CharField(max_length=30, verbose_name='负责人')),
                ('dept_position', models.CharField(max_length=10, verbose_name='职务')),
                ('boos_phone', models.CharField(max_length=11, verbose_name='联系电话')),
            ],
            options={
                'verbose_name': '部门',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=11, unique=True, verbose_name='员工工号')),
                ('member_avatar', models.ImageField(blank=True, default='none', null=True, upload_to='avatar', verbose_name='头像')),
                ('name', models.CharField(max_length=50, null=True, verbose_name='姓名')),
                ('nation', models.CharField(default='汉', max_length=10, verbose_name='民族')),
                ('blood_type', models.CharField(default='未知', max_length=10, verbose_name='血型')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], default=' ', max_length=5, verbose_name='性别')),
                ('birthday', models.CharField(default=' ', max_length=50, verbose_name='出生年月')),
                ('position', models.CharField(default=' ', max_length=50, verbose_name='职位')),
                ('phone', models.CharField(default=' ', max_length=11, verbose_name='联系方式')),
                ('dept', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Departments', verbose_name='部门')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
                'ordering': ['member_id'],
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='权限名称')),
                ('url', models.CharField(max_length=255, verbose_name='含正则的URL')),
                ('code', models.CharField(max_length=32, verbose_name='权限代码')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
                ('permissions', models.ManyToManyField(to='member.Permission', verbose_name='拥有权限')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='roles',
            field=models.ManyToManyField(blank=True, to='member.Role', verbose_name='拥有角色'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_dept',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='member.Departments', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
