from datetime import timedelta

from django.utils import timezone
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponse
from django.shortcuts import render
from .models import *


def passes_by_hour(passes):
    pass_by_hour = dict()
    for i in range(1, 25):
        p = Passes.objects.filter(time_of_pass__hour=i, light_id=679185593).count()
        pass_by_hour[i] = p
    return pass_by_hour


def all_locations(request):
    locations = Location.objects.all()
    return render(request, 'locations.html', {'locations': locations})


def display_window(request):
    tajp = Type.objects.get(type='display')
    light = Light.objects.get(id=679185593)
    passing = Passes.objects.filter(light=light)
    views = passing.filter(duration__gt=100).count()
    p_hour = passes_by_hour(passing)
    v_hour = passes_by_hour(views)
    wake_time = [ele.duration for ele in passing]
    print(wake_time)
    sleep_time = 8 - sum(wake_time) / 3600
    C02 = 0.869  # kg/MWh
    one_tree_per_year = 167  # kg/year
    one_tree_per_day = one_tree_per_year / 365
    not_comsumed = light.power * sleep_time * 10 ** (-6)
    green = not_comsumed * C02
    trees = green / one_tree_per_day
    passing_by = passing.count()
    return {'display_light': light,
            'passes': passing,
            'passes_by_hour': p_hour,
            'views': views,
            'views_by_hour': v_hour,
            'sleep_time': str(sleep_time)[:3],
            'CO2': str(green)[:8],
            'trees': trees,
            'passing_by':passing_by
            }


def add_pass(request):
    mesh_id = request.GET.get('id')
    time = timezone.now()
    duration = float(request.GET.get('duration'))
    temperature = float(request.GET.get('temperature'))
    brightness = float(request.GET.get('brightness'))
    pressure = float(request.GET.get('pressure'))
    humidity = float(request.GET.get('humidity'))
    try:
        light = Light.objects.get(mesh_id=mesh_id)
        view = Passes.objects.create(light=light,
                                     time_of_pass=time,
                                     duration=duration,
                                     temperature=temperature,
                                     brightness=brightness,
                                     pressure=pressure,
                                     humidity=humidity)
        view.save()
        return HttpResponse('success')
    except Exception as e:
        print(e)
        return HttpResponse('failed')


def street_light(request):
    # tajp = Type.objects.get(type='street')
    light = Light.objects.get(id=2040916967)
    passes = Passes.objects.filter(light=light, time_of_pass__gt=timezone.now() - timedelta(days=1))
    times = [str(i.hour) + ":" + str(i.minute) for i in
             passes.order_by('time_of_pass').values_list('time_of_pass', flat=True)]
    temperature = [float(i) for i in passes.order_by('time_of_pass').values_list('temperature', flat=True) if i is not None]
    brightness = [float(i) for i in passes.order_by('time_of_pass').values_list('brightness', flat=True) if i is not None]
    pressure = [float(i) for i in passes.order_by('time_of_pass').values_list('pressure', flat=True) if i is not None]
    humidity = [float(i) for i in passes.order_by('time_of_pass').values_list('humidity', flat=True) if i is not None]
    air_quality = [float(i) for i in passes.order_by('time_of_pass').values_list('air_quality', flat=True) if i is not None]
    print(brightness)
    return {'street_light': light,
            'passes_street': passes,
            'time': times,
            'temperature': temperature,
            'brightness': brightness,
            'pressure': pressure,
            'humidity': humidity,
            'air': air_quality}


def landing(request):
    display = display_window(request)
    street = street_light(request)
    both = {**display, **street}
    return render(request, 'landing.html', both)
