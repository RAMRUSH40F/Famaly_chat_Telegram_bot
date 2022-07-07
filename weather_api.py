import requests
from datetime import datetime
from config import weather_api_id


def convert_time(time):
    ts = int(time)
    return datetime.utcfromtimestamp(ts).strftime('%H:%M')


def get_weather():
    api_url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'q': 'Saint Petersburg',
        'appid': weather_api_id,
        'lang': 'ru',
        'units': 'metric'
    }
    res = requests.get(api_url, params=params)
    res = res.json()
    # print(res)
    weather = f"Температура за окном +{res['main']['temp']}. Ощущается как +{str(res['main']['feels_like'])[0]}.\n " \
              f"{res['weather'][0]['description']}. Солнце зайдет в {convert_time(res['sys']['sunset'])} "
    icon_path_in_folder = 'icons/{}@2x.png'.format(res['weather'][0]['icon'])
    return([weather, icon_path_in_folder])


if __name__ == '__main__':
    weather, path = get_weather()
    print(weather, path)
    # 04d@2x.png
