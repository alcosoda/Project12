from flask import Flask, render_template, request

from logic import get_location_key, get_weather_forecast, check_bad_weather

app = Flask(__name__)

api_key = "jUkVAUIEU557aaZYLpcGDVPgu7ulY5UO"  # Твой API ключ


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        weather_data = []

        # Get the number of locations from the form data
        num_locations = sum(1 for key in request.form if key.startswith("city"))

        for i in range(1, num_locations + 1):
            city = request.form.get(f"city{i}")
            date_offset = int(request.form.get(f"date{i}", 0))

            location_key = get_location_key(api_key, city)
            if location_key:
                forecast = get_weather_forecast(api_key, location_key, date_offset)
                weather_status = check_bad_weather(forecast)
                weather_data.append({
                    "city": city,
                    "weather_status": weather_status,
                    "forecast": forecast
                })
            else:
                weather_data.append({
                    "city": city,
                    "weather_status": "Город не найден",
                    "forecast": None
                })

        return render_template("result.html", weather_data=weather_data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)