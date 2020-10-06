from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, NoReverseMatch

from .weather_check import hyper_weather_check


def index(requests):
    if requests.POST:
        try:
            return redirect('weather:info', requests.POST['text'])
        except NoReverseMatch:
            return render(requests, 'weather/index.html')
    return render(requests, 'weather/index.html')


def info(requests, city):
    city_info = hyper_weather_check(city)
    try:
        context = {
            'city_now': city_info['now'],
            'city_hourly': city_info['hourly'],
            'city_daily': city_info['daily'],
        }
        return render(requests, 'weather/info.html', context=context)
    except KeyError:
        context = {
            'error': 'Ошибка: Введенные данные некорректны'
        }
        return render(requests, 'weather/info.html', context=context)
