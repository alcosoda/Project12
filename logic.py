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


def get_weather_forecast(api_key, location_key, date_offset=0):
    if location_key is None:
        return None

    # Use the 5-day forecast API
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={api_key}&metric=true&details=true"

    try:
        response = requests.get(url)
        response.raise_for_status()
        forecast_data = response.json()

        # Get the forecast for the specified date offset
        if 0 <= date_offset < len(forecast_data['DailyForecasts']):
            return forecast_data['DailyForecasts'][date_offset]
        else:
            raise ValueError("Invalid date_offset. It should be within the range of available forecasts.")

    except requests.exceptions.RequestException as e:
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
            # Adding more parameters
            forecast.get('Day', {}).get('SnowProbability', 0) > 50 or  # Snow probability > 50%
            forecast.get('Day', {}).get('Visibility', {}).get('Value', float('inf')) < 1 or  # Visibility < 1 km
            forecast.get('Day', {}).get('UVIndex', 0) > 7  # UV Index > 7
            ):
        # Формируем более информативное сообщение о плохой погоде
        bad_weather_reasons = []
        # Add more detailed bad weather reasons:
        if temperature < 0:
            bad_weather_reasons.append(f"слишком холодно ({temperature}°C)")
        if temperature > 35:
            bad_weather_reasons.append(f"слишком жарко ({temperature}°C)")
        if wind_speed > 50:
            bad_weather_reasons.append(f"сильный ветер ({wind_speed} км/ч)")
        # ... (similarly for other parameters) ...
        if rain_probability > 70:
            bad_weather_reasons.append("высокая вероятность дождя")
        if forecast.get('Day', {}).get('SnowProbability', 0) > 50:
            bad_weather_reasons.append("высокая вероятность снега")
        if forecast.get('Day', {}).get('Visibility', {}).get('Value', float('inf')) < 1:
            bad_weather_reasons.append("плохая видимость")
        if forecast.get('Day', {}).get('UVIndex', 0) > 7:
            bad_weather_reasons.append("высокий UV индекс")
        # ... (добавляем причины для других параметров) ...

        return f"Ой-ой, погода плохая: {', '.join(bad_weather_reasons)}." if bad_weather_reasons else "Погода — супер"

    else:
        return "Погода — супер"