# Generated by Django 4.0.4 on 2022-05-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lightsoff', '0003_light_power'),
    ]

    operations = [
        migrations.AlterField(
            model_name='light',
            name='power',
            field=models.PositiveIntegerField(verbose_name='Power in watts'),
        ),
    ]
