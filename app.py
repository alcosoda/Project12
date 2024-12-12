from flask import Flask, render_template, request
from logic import Connect, Weather

app = Flask(__name__)
api_key = 'Jul2EgzWSP0sgvNojXxIAbzCEJmMSlrq'  # Replace with your AccuWeather API key

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        try:
            cities = request.form.getlist('cities[]')
            weather_data = {}

            for city in cities:
                api = Connect(api_key=api_key)
                weather_lst = api.get_weather(city)

                weather_data[city] = []
                for item in weather_lst:
                    item.info = item.validate()
                    weather_data[city].append(item)

            return render_template('index.html', weather_data=weather_data, format={'Day': 'День', 'Night': 'Ночь'})

        except KeyError:
            return render_template('error_message.html', msg='В форме не хватает полей')
        except IndexError:
            return render_template('error_message.html', msg='Город не найден')
        except Exception:
            return render_template('error_message.html', msg='Не удаётся подключиться к API')

    return render_template('input.html')

if __name__ == '__main__':
    app.run()