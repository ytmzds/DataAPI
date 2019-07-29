from flask import Flask
import changerate
import oil
import oilandgold
import weather
import stock

app = Flask(__name__)

@app.route('/')
def hello():
    return "API"

@app.route('/find_changerate/<c>')
def change(c):
    return changerate.getmoney(c)

@app.route('/oil')
def _oil():
    return oil.getOilPrice()

@app.route('/gold')
def gold():
    return oilandgold.GetGoldData()

@app.route('/find_city/<cityy>')
def _weather(cityy):
    return weather.getWeather(cityy)

@app.route('/find_code/<code>')
def _stock(code):
    return stock.getstock(code)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug = True)
