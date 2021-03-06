# Generated by Django 4.0.4 on 2022-05-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lightsoff', '0006_remove_light_temperature_passes_temperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='passes',
            name='air_quality',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='passes',
            name='brightness',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='passes',
            name='humidity',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='passes',
            name='pressure',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='passes',
            name='duration',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Duration in seconds'),
        ),
    ]
