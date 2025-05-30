from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv('OPENWEATHER_API_KEY')

def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast_data(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def filter_forecast_by_noon(forecast_list):
    return [entry for entry in forecast_list if "12:00:00" in entry["dt_txt"]]

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    location = ""
    error_message = None
    condition = "default"

    if request.method == "POST":
        location = request.form.get("location")
        if location:
            weather_data = get_weather_data(location)
            forecast_raw = get_forecast_data(location)

            if weather_data.get("cod") != 200:
                error_message = weather_data.get("message", "Invalid location or API error")
                weather_data = None
                forecast_data = None
            else:
                forecast_data = filter_forecast_by_noon(forecast_raw.get("list", []))
                condition = weather_data["weather"][0]["main"].lower()

    return render_template("index.html", weather=weather_data, forecast=forecast_data,
                           location=location, error=error_message, condition=condition)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)