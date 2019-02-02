# Generated by Django 2.1.3 on 2019-01-16 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialstock',
            old_name='num',
            new_name='count',
        ),
        migrations.AlterField(
            model_name='materialstock',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='record', to='material.Material'),
        ),
    ]
