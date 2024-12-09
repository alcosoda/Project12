import requests

def get_location_key(api_key, city):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={api_key}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data[0]['Key']

def get_weather_forecast(api_key, location_key):
    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={api_key}&metric=true"
    response = requests.get(url)
    forecast_data = response.json()
    return forecast_data['DailyForecasts'][0]

def check_bad_weather(forecast):
    temperature = forecast['Temperature']['Maximum']['Value']
    wind_speed = forecast['Day']['Wind']['Speed']['Value']
    rain_probability = forecast['Day']['RainProbability']

    if temperature < 0 or temperature > 35 or wind_speed > 50 or rain_probability > 70:
        return "Ой-ой, погода плохая"
    else:
        return "Погода — супер"