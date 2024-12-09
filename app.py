from flask import Flask, render_template, request
from logic import get_location_key, get_weather_forecast, check_bad_weather
import requests
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'}) # Используем простое кэширование

api_key = "1aVr87Bt3NlBICxPnuqQlqNXGkk4o6Rv"  # Твой API ключ

@app.route("/", methods=["GET", "POST"])
@cache.cached(timeout=3600)  # Кэшируем результаты на 1 час
def index():
    if request.method == "POST":
        city = request.form["city"]
        location_key = get_location_key(api_key, city)
        if location_key is None:
            return render_template("error.html", message="Город не найден или произошла ошибка при получении данных.")
        forecast = get_weather_forecast(api_key, location_key)
        if forecast is None:
            return render_template("error.html", message="Произошла ошибка при получении прогноза погоды.")
        try:
            weather_status = check_bad_weather(forecast)
            return render_template("result.html", city=city, weather_status=weather_status)
        except Exception as e:  # Обрабатываем любые исключения
            print(f"Произошла ошибка: {e}")
            return render_template("error.html", message="Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)