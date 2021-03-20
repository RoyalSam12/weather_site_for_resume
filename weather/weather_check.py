from time import ctime

import requests


def hyper_weather_check(city):
    api_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': 'fe6c9ac08e96ecdd33f559f07bc59da7',
        'units': 'metric',
        'lang': 'ru'
    }
    re = requests.get(api_url, params=params)
    if re.status_code == 404:
        data_for_views = {'get_info': False, 'error': 'Данные введены некорректно'}
        return data_for_views
    else:
        data_for_views = dict()
        data = re.json()
        data_lon = data['coord']['lon']
        data_lat = data['coord']['lat']
        data_for_views['now'] = {
            'city_name': data['name'],
            'weather_description': data['weather'][0]['description'].capitalize(),
            'weather_temp': data['main']['temp'],
            'weather_feels_temp': data['main']['feels_like'],
            'wind_speed': data['wind']['speed']
        }
        api_url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {
            'lon': data_lon,
            'lat': data_lat,
            'appid': 'fe6c9ac08e96ecdd33f559f07bc59da7',
            'units': 'metric',
            'lang': 'ru'
        }
        re = requests.get(api_url, params=params)
        data = re.json()
        data_for_views['hourly'] = dict()
        for day_info in data['hourly']:
            data_for_views['hourly'][ctime(day_info['dt'])[11:16]] = {
                'time': ctime(day_info['dt'])[11:16],
                'temp_day': day_info['temp'],
                'feels_temp_day': day_info['feels_like'],
                'wind_speed': day_info['wind_speed'],
                'weather_description': day_info['weather'][0]['description'].capitalize()
            }
            if ctime(day_info.get('dt'))[11:16] == '23:00':
                break
        data_for_views['daily'] = dict()
        for day_info in data['daily']:
            data_for_views['daily'][ctime(day_info['dt'])] = {
                'day_of_week': ctime(day_info.get('dt'))[:10],
                'temp_day': day_info['temp']['day'],
                'temp_night': day_info['temp']['night'],
                'temp_eve': day_info['temp']['eve'],
                'temp_morn': day_info['temp']['morn'],
                'feels_temp_day': day_info['feels_like']['day'],
                'feels_temp_night': day_info['feels_like']['night'],
                'feels_temp_eve': day_info['feels_like']['eve'],
                'feels_temp_morn': day_info['feels_like']['morn'],
                'weather_description': day_info['weather'][0]['description'].capitalize()
            }
        return data_for_views
