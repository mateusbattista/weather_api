
import requests
from flask import Flask, request, render_template, flash
from wtforms import Form, validators, TextField


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class CityForm(Form):
    city = TextField('Cidade', validators=[validators.required()])

    @app.route('/city', methods=['GET', 'POST'])
    def search_city():
        form = CityForm(request.form)
        if request.method == 'POST':
            API_KEY = '10f0c78e4aeae6a129ea22fbac129054'  # initialize your key here
            city = request.form['city']  # city name passed as argument

            if form.validate():
                # call API and convert response into Python dictionary
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={API_KEY}'
                response = requests.get(url).json()

                # error like unknown city name, inavalid api key
                if response.get('cod') != 200:
                    message = response.get('message', '')
                    flash(f'Error getting temperature for {city.title()}. Error message = {message}')

                # get current temperature and convert it into Celsius
                current_temperature = response.get('main', {}).get('temp')
                if current_temperature:
                    current_temperature_celsius = round(current_temperature - 273.15, 2)
                    flash(f'Current temperature of {city.title()} is {current_temperature_celsius} Cº')
                else:
                    flash(f'Error getting temperature for {city.title()}')
            else:
                flash('Preencha o nome da cidade')
        return render_template('city.html', form=form)



@app.route('/')
def index():
    return '<h1>Welcome to weather app</h1>'


if __name__ == '__main__':
    app.run(debug=True)


