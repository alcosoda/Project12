import requests


def get_location_key(api_key, city):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
        data = response.json()
        if data:
            return data[0]['Key']
        else:
            raise ValueError("Город не найден")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Ошибка при получении ключа локации: {e}")
        return None  # Возвращаем None в случае ошибки


def get_weather_forecast(api_key, location_key):
    if location_key is None:
        return None
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&metric=true&details=true"
    try:
        response = requests.get(url)
        response.raise_for_status()
        forecast_data = response.json()
        return forecast_data['DailyForecasts'][0]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении прогноза погоды: {e}")
        return None

def check_bad_weather(forecast):
    temperature = forecast['Temperature']['Maximum']['Value']
    wind_speed = forecast['Day']['Wind']['Speed']['Value']
    rain_probability = forecast['Day']['RainProbability']

    if temperature < 0 or temperature > 35 or wind_speed > 50 or rain_probability > 70:
        return "Ой-ой, погода плохая"
    else:
        return "Погода — супер"