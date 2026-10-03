from services.openweather_api import get_weather
from services.files import create_file
from services.dashboard import render
from services.mysql_db import create_weather_table, save_weather
import time

# Wyświetlanie dashboardu
# render()

# Tworzenie tabeli SQL
create_weather_table()

while True:
  # Pobieranie danych pogodowych
    weather = get_weather()
    # Zapisywanie w xlsx
    create_file([weather])
    # Zapisywanie w SQL
    save_weather(weather)
    print("Pobrałem dane")
    time.sleep(120)


