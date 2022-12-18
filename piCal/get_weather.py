import json

import requests

def get_weather():
    api_key = 'a9476947fa1a2f712076453bec4a0df5'

    # kilburn lat and long
    lat = 51.5398
    lon = 0.1985
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&units=metric&lon={}&appid={}'.format(lat, lon,
                                                                                                       api_key)
    r = requests.get(url)

    daily_weather = []
    daily = r.json()['daily']

    for day in daily:
        dct = {}
        dct['main_weather'] = day['weather'][0]['main']
        dct['description'] = day['weather'][0]['description']
        dct['min_temp'] = day['temp']['min']
        dct['max_temp'] = day['temp']['max']
        daily_weather.append(dct)


    return daily_weather


weather = get_weather()
json.dump(weather, open('data/weather.json', 'w+'))


