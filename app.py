from flask import Flask, render_template, request

from logic import get_location_key, get_weather_forecast, check_bad_weather

app = Flask(__name__)

api_key = "jUkVAUIEU557aaZYLpcGDVPgu7ulY5UO"  # Твой API ключ

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        location_key = get_location_key(api_key, city)
        forecast = get_weather_forecast(api_key, location_key)
        weather_status = check_bad_weather(forecast)
        return render_template("result.html", city=city, weather_status=weather_status)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)