
from pathlib import Path

import requests
from celery import shared_task
from django.conf import settings


@shared_task
def request_to_api():
    file_path = Path(
        settings.BASE_DIR, 'main', 'weather_json', 'response.json')
    url = 'https://api.weather.yandex.ru/v2/forecast'
    params = {'lat': 59.9343, 'lon': 30.3351, 'extra': 'False'}
    headers = {'x-Yandex-API-Key': 'ваш ключ'}

    response = requests.get(url, params=params, headers=headers)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)
