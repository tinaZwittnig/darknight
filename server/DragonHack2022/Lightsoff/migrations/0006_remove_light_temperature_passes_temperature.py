# Generated by Django 4.0.4 on 2022-05-14 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lightsoff', '0005_alter_light_id_alter_location_id_alter_passes_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='light',
            name='temperature',
        ),
        migrations.AddField(
            model_name='passes',
            name='temperature',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
