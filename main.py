import requests
import pandas as pd
from datetime import datetime
from flask import Flask, request, render_template
import os

weather_icons = os.path.join('static', 'icons')
backrounds = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = weather_icons
app.config['BACKGROUND_FOLDER'] = backrounds

@app.route('/')
def my_form():

    gradient = "linear-gradient(to top, #4b6cb7, #182848);"

    return render_template('form2.html',gradient=gradient)

@app.route('/', methods=['POST'])
def weather_now():
    
    text = request.form['text']

    if text == '':
        gradient = "linear-gradient(to top, #4b6cb7, #182848);"
        return render_template('form2.html',out="empty",gradient=gradient)
    else:

        url = "http://api.openweathermap.org/data/2.5/weather?q={!s}&units=metric&appid=****".format(text) # API key is hidden
        response = requests.request("GET", url)

        json = response.json()


        if json['cod'] == '404':
            gradient = "linear-gradient(to top, #4b6cb7, #182848);"
            return render_template('form2.html',out="not",gradient=gradient)
        else:
            weather = json['weather']

            id = str(weather[0]['id'])

            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '{!s}.png').format(id)

            uid = weather[0]['id']


            if uid < 300:
                gradient = "linear-gradient(to top, #373b44, #4286f4);"
            elif uid > 300 and uid < 500:
                gradient = "linear-gradient(to top, #E7E9BB, #403B4A);"
            elif uid > 500 and uid < 505:
                gradient = "linear-gradient(to top, #E5E5BE, #003973);"
            elif uid == 511:
                gradient = "linear-gradient(to top, #03588C, #0D4C73);"
            elif uid > 519 and uid < 532:
                gradient = "linear-gradient(to top, #021B79, #0575E6);"
            elif uid > 532 and uid < 623:
                gradient = "linear-gradient(to top, #2a5298, #1e3c72);"
            elif uid > 624 and uid < 782:
                gradient = "linear-gradient(to top, #2c3e50, #bdc3c7);"
            elif uid == 800:
                gradient = "linear-gradient(to bottom, #00416a, #799f0c, #ffe000);"
            elif uid == 801:
                gradient = "linear-gradient(to bottom, #00467F, #A5CC82);"
            elif uid == 802:
                gradient = "linear-gradient(to bottom, #005C97, #363795);"
            elif uid == 803 or uid == 804:
                gradient = "linear-gradient(to bottom, #4b6cb7, #182848);"


            
            description = weather[0]['description'].title()
            main = json['main']

            temp = main['temp']
            feels_like = main['feels_like']

            wind = json['wind']
            wind_speed = wind['speed']

            humidity = main['humidity']

            def wind_category(speed):
                if speed < 5:
                    return "Very slow wind"
                elif speed < 10 and speed > 5: 
                    return "Rather slow wind"
                elif speed < 20 and speed > 10:
                    return "Considerable wind, may lead to difficulties"
                elif speed < 30 and speed > 20:
                    return "Very windy, caution is advised"
                elif speed > 30:
                    return "Extreme wind, dangerous"

            wind_description = wind_category(wind_speed)

            city_name = json['name']

            sys = json['sys']

            country = sys['country']

            city_country = ("%s, %s " %(city_name,country))



            # future weather #

            coord = json['coord']

            lon = coord['lon']

            lat = coord['lat']

            url_future = "https://api.openweathermap.org/data/2.5/onecall?lat={!s}&lon={!s}&exclude=minutely,hourly&units=metric&appid=0a6abea71fc7316fdbb2bd0128ce5652".format(lat,lon)

            response_future = requests.request("GET", url_future)

            json_future = response_future.json()

            daily = json_future['daily']

            i = 1
            future = []
            while i < 8:
                first = daily[i]

                weather_future = first['weather']
                ids = str(weather_future[0]['id'])

                future_full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '{!s}.png').format(ids)

                future_temp = first['temp']
                future_day_temp = future_temp['max']
                future_night_temp = future_temp['min']
                future_humidity = first['humidity']
                
                future_weather = first['weather']
                future_weather_description = future_weather[0]['description']

                future_wind_speed = first['wind_speed']
                future_wind_description = wind_category(future_wind_speed)
                
                dates = first['dt']
                ts = int(dates)
                day = datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                day_name = pd.to_datetime(day).day_name()

                if day_name == "Monday":
                    day_name_short = "Mon"
                elif day_name == "Tuesday":
                    day_name_short = "Tue"
                elif day_name == "Wednesday":
                    day_name_short = "Wed"
                elif day_name == "Thursday":
                    day_name_short = "Thur"
                elif day_name == "Friday":
                    day_name_short = "Fri"
                elif day_name == "Saturday":
                    day_name_short = "Sat"
                elif day_name == "Sunday":
                    day_name_short = "Sun"


                # ("%s \nDay Temperature: %d°C \nNight Temperature: %d°C \nDescription: %s \nWind: %s (%s m/s) \nHumidity: %s%% \n" %(day_name,int(future_day_temp),int(future_night_temp),future_weather_description,future_wind_description,future_wind_speed,future_humidity ))

                i += 1

                day = {
                "day_name": day_name_short,
                "day_temperature": int(future_day_temp),
                "night_temperature": int(future_night_temp),
                "description": future_weather_description,
                "wind_Decription": future_wind_description,
                "wind_Speed": future_wind_speed,
                "humidity": future_humidity,
                "ids": ids,
                "sources":future_full_filename
                }

                future.append(day)

            # end future wearher #
            
            return render_template('form2.html',
                out='good',
                city_name=city_country,
                temp=int(temp),
                feels_like=int(feels_like),
                description=description,
                wind_description=wind_description,
                wind_speed=wind_speed,
                humidity=humidity,
                future=future,
                id=id,
                source=full_filename,
                gradient=gradient
            )

if __name__ == '__main__':
    app.run(debug=True)
