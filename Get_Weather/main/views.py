import json
from pathlib import Path

import requests
from django.conf import settings
from django.shortcuts import render

translate = {"clear": 'ясно',
             'partly-cloudy': 'малооблачно',
             'cloudy': 'облачно с прояснениями',
             'overcast': 'пасмурно',
             'light-rain': 'небольшой дождь',
             'rain': 'дождь',
             'heavy-rain': 'сильный дождь',
             'showers': 'ливень',
             'wet-snow': 'дождь со снегом',
             'light-snow': 'небольшой снег',
             'snow': 'снег',
             'snow-showers': 'снегопад',
             'hail': 'град',
             'thunderstorm': 'гроза',
             'thunderstorm-with-rain': 'дождь с грозой',
             'thunderstorm-with-hail': 'гроза с градом'}


def request_to_api():
    file_path = Path(
        settings.BASE_DIR, 'main', 'weather_json', 'response.json')
    url = 'https://api.weather.yandex.ru/v2/forecast'
    params = {'lat': 59.9343, 'lon': 30.3351, 'extra': 'False'}
    headers = {'x-Yandex-API-Key': 'e286f6c4-74f7-4f94-aa95-7c17ca883134'}

    response = requests.get(url, params=params, headers=headers)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)


def context_formation(translate):
    file_path = Path(
        settings.BASE_DIR, 'main', 'weather_json', 'response.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    context = {}
    days = {}
    image_url = 'https://yastatic.net/weather/i/icons/funky/dark/'
    pogoda = data.get('forecasts')
    i = 1
    for day in pogoda:
        day_weather = day.get('parts').get('day')
        night_weather = day.get('parts').get('night')
        days.update({'date' + str(i): [day.get("date"),
                                       day_weather.get('temp_avg'),
                                       day_weather.get('temp_min'),
                                       day_weather.get('temp_max'),
                                       night_weather.get('temp_avg'),
                                       night_weather.get('temp_min'),
                                       night_weather.get('temp_max'),
                                       day_weather.get('feels_like'),
                                       night_weather.get('feels_like'),
                                       translate.get(
                                           day_weather.get('condition')),
                                       translate.get(
                                           night_weather.get('condition')),
                                       image_url + day_weather.get(
                                           'icon') + '.svg',]})
        i += 1
    context['days'] = days
    return context


def main(request):
    context = context_formation(translate)
    return render(request, 'pogoda.html', context)
