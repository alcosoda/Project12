from flask import Flask, render_template, request

from logic import Connect, Weather # Импортируем классы из logic.py

app = Flask(__name__)

api_key = 'Jul2EgzWSP0sgvNojXxIAbzCEJmMSlrq'


@app.route('/', methods=['GET'])
def main_page():
    return render_template('input.html')


@app.route('/', methods=['POST'])
def main_page_post():
    try:
        form = request.form
        point_start, point_end = form['point_start'], form['point_end']

        api = Connect(api_key=api_key)
        start_lst = api.get_weather(point_start)
        end_lst = api.get_weather(point_end)

        weather_start = [item for item in start_lst]
        weather_end = [item for item in end_lst]

        for item in weather_start:
            item.info = item.validate()
        for item in weather_end:
            item.info = item.validate()

    except KeyError:
        return render_template('error_message.html', msg='В форме не хватает полей')
    except IndexError:
        return render_template('error_message.html', msg='Город не найден')
    except Exception:
        return render_template('error_message.html', msg='Не удаётся подключиться к API')
    return render_template('index.html', start=weather_start, end=weather_end,
                           format={'Day': 'День', 'Night': 'Ночь'})


if __name__ == '__main__':
    app.run()