from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/weather', methods=['POST'])
def weather():
    try:    #Probability of KeyError if name of city is incorrect
        city = request.form['city'] #Getting city from user's input

        authCode = '5b3c9e156080a5b189cdae8794702601' #authorization code for OpenWeatherMap
        textForRequest = 'http://api.openweathermap.org/data/2.5/weather' + '?q=' + city + '&appid=' + authCode
        resp = requests.get(textForRequest)

        #Coordinates for the city
        coordLon = resp.json()['coord']['lon']
        coordLat = resp.json()['coord']['lat']

        #Temperature for the city (from Farenheit into Celcius)
        temperature = str(round(float(resp.json()['main']['temp'])-273.15, 2))
        temperatureFeels = str(round(float(resp.json()['main']['feels_like'])-273.15, 2))
    
        #Getting other values - humidity, pressure and wind speed
        humidity = resp.json()['main']['humidity']
        pressure = resp.json()['main']['pressure']
        wind = resp.json()['wind']['speed']

        #Getting name of the icon to display
        icon = '../static/' + resp.json()['weather'][0]['icon'] + '.jpg'

        #Rendering template with values from json file
        return render_template('/weather.html', city=city, lon=coordLon, lat=coordLat, temp=temperature,
                              tempFeels=temperatureFeels, humid=humidity, press=pressure, wind=wind, image=icon)
    except KeyError: #Rendering template with error
        return render_template('/weather.html', city='KeyError, wrong city name')



@app.route('/')
def home(): #Rendering homepage template
    return render_template('/home.html')


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
