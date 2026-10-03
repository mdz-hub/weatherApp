import requests
from config import App
from datetime import datetime, timezone
from common.functions import from_ts,from_kel_to_cel,from_ms_to_kmh

def get_weather():
    KEY = App.OW_API_KEY
    CITY = App.OW_CITY
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={KEY}"

    try:
        response = requests.get(URL)
        data = response.json()
        weather = {
            "temp": from_kel_to_cel(data.get("main").get("temp")),
            "feels_like": from_kel_to_cel(data.get("main").get("feels_like")),
            "humidity": data.get("main").get("humidity"),
            "pressure": data.get("main").get("pressure"),
            "wind": from_ms_to_kmh(data.get("wind").get("speed")),
            "clouds": data.get("clouds").get("all"),
            "city": data.get("name"),
            "sunrise": from_ts(data.get("sys").get("sunrise")),
           "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather
    except Exception as err:
        print(err)

def get_weather2():
    KEY = App.OW_API_KEY
    CITY2 = App.OW_CITY2
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY2}&appid={KEY}"

    try:
        response = requests.get(URL)
        data2 = response.json()
        weather2 = {
            "temp": from_kel_to_cel(data2.get("main").get("temp")),
            "feels_like": from_kel_to_cel(data2.get("main").get("feels_like")),
            "humidity": data2.get("main").get("humidity"),
            "pressure": data2.get("main").get("pressure"),
            "wind": from_ms_to_kmh(data2.get("wind").get("speed")),
            "clouds": data2.get("clouds").get("all"),
            "city": data2.get("name"),
            "sunrise": from_ts(data2.get("sys").get("sunrise")),
           "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return weather2
    except Exception as err:
        print(err)