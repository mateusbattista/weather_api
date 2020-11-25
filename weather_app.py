
import requests
from flask import Flask, request, render_template, flash
from wtforms import Form, validators, TextField
from flask_caching import Cache

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)

# tell Flask to use the above defined config
app.config.from_mapping(config)
cache = Cache(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class CityForm(Form):
    city = TextField('Cidade', validators=[validators.required()])
    
    @cache.cached(timeout=900)
    @app.route('/city', methods=['GET', 'POST'])
    def search_city():
        form = CityForm(request.form)
        if request.method == 'POST':
            API_KEY = '10f0c78e4aeae6a129ea22fbac129054'  # initialize your key here
            city = request.form['city']  # city name passed as argument
            LANG = 'pt_br'

            if form.validate():
                # call API and convert response into Python dictionary
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&lang={LANG}&APPID={API_KEY}'
                response = requests.get(url).json()
                # error like unknown city name, inavalid api key
                if response.get('cod') != 200:
                    message = response.get('message', '')
                    flash(f'Error getting temperature for {city.title()}. Error message = {message}')

                # get current temperature and convert it into Celsius
                current_temperature = response.get('main', {}).get('temp')
                clima = response.get('weather', {})[0].get('main')
                descricao_clima = response.get('weather', {})[0].get('description')
                
                flash(clima)
                flash(descricao_clima)
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


