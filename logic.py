from datetime import datetime
import requests

class Connect:
    def __init__(
            self,
            api_key,
            address='http://dataservice.accuweather.com/'
    ):
        self.address = address
        self.api_key = api_key

    def get_key(self, city):
        req = requests.get(url=f'{self.address}locations/v1/cities/search',
                           params={
                               'apikey': self.api_key,
                               'q': city,
                               'language': 'en-us',
                               'details': 'true'
                           })
        res = req.json()
        return res[0]['Key']

    def get_weather(self, city):
        location_key = self.get_key(city)
        req = requests.get(url=f'{self.address}forecasts/v1/daily/5day/{location_key}',
                           params={
                               'apikey': self.api_key,
                               'language': 'en-us',
                               'details': 'true',
                               'metric': 'true'
                           })
        res = req.json()
        lst = list()
        for day in res['DailyForecasts']:
            for day_part in ['Day', 'Night']:
                lst.append(
                    Weather(date=datetime.fromisoformat(day['Date']).date(),
                            part=day_part,
                            location=city,
                            rain=day[day_part]['RainProbability'],
                            humidity=day[day_part]['RelativeHumidity']['Average'],
                            wind=day[day_part]['Wind']['Speed']['Value'],
                            temp_c=(day['Temperature']['Minimum']['Value'] +
                                    day['Temperature']['Maximum']['Value']) / 2)
                )
        return lst


class Weather:
    def __init__(self, location, date, part, rain, humidity, temp_c, wind):
        self.location = location
        self.date = date
        self.part = part
        self.rain = rain
        self.humidity = humidity
        self.temp_c = temp_c
        self.wind = wind
        self.info = None

    def validate(self):
        if self.temp_c < 0:
            return 'Брррр как холодно'
        elif self.temp_c > 40:
            return 'Банька с дедом'
        if self.wind > 50:
            return 'Ветер сносит шляпы и задирает платья'
        if self.humidity < 20:
            return 'Сухо как в Сахаре'
        if self.rain > 70:
            return 'Кажется кто-то рядом танцует танец дождя'
        return 'Погодка сойдёт'