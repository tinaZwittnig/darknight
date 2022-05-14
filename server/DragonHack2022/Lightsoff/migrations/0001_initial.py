# Generated by Django 4.0.4 on 2022-05-14 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesh_id', models.PositiveIntegerField()),
                ('temperature', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=100)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=100)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('display', 'display window'), ('street', 'street light')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Passes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_pass', models.DateTimeField()),
                ('duration', models.PositiveIntegerField(verbose_name='Duration in seconds')),
                ('light', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Lightsoff.light')),
            ],
        ),
        migrations.AddField(
            model_name='light',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lightsoff.location'),
        ),
        migrations.AddField(
            model_name='light',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Lightsoff.type'),
        ),
    ]