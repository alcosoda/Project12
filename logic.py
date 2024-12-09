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
        # Проверка на наличие необходимых ключей в данных прогноза
        required_keys = ['DailyForecasts', 'Temperature', 'Day', 'Wind', 'RainProbability', 'CloudCover', 'TotalLiquid']
        if not all(key in forecast_data for key in required_keys):
            raise ValueError("Невалидные данные прогноза погоды")  # Выбрасываем исключение, если данные неполные
        return forecast_data['DailyForecasts'][0]
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Ошибка при получении прогноза погоды: {e}")
        return None




def check_bad_weather(forecast):
    temperature = forecast['Temperature']['Maximum']['Value']
    wind_speed = forecast['Day']['Wind']['Speed']['Value']
    rain_probability = forecast['Day']['RainProbability']

    # Добавляем больше параметров для оценки погоды
    # Например, учитываем облачность, осадки и видимость
    cloud_cover = forecast['Day']['CloudCover']
    total_liquid = forecast['Day']['TotalLiquid']['Value']
    # Проверка на наличие данных о видимости
    visibility = forecast['Day']['Visibility']['Value'] if 'Visibility' in forecast['Day'] else None

    if (temperature < 0 or temperature > 35 or
            wind_speed > 50 or rain_probability > 70 or
            cloud_cover > 80 or total_liquid > 5 or
            visibility < 1):
        # Формируем более информативное сообщение о плохой погоде
        bad_weather_reasons = []
        if temperature < 0:
            bad_weather_reasons.append("слишком холодно")
        if temperature > 35:
            bad_weather_reasons.append("слишком жарко")
        if wind_speed > 50:
            bad_weather_reasons.append("сильный ветер")
        if rain_probability > 70:
            bad_weather_reasons.append("высокая вероятность дождя")
        # ... (добавляем причины для других параметров) ...

        return f"Ой-ой, погода плохая: {', '.join(bad_weather_reasons)}."
    else:
        return "Погода — супер"