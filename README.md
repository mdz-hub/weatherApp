Przejrzałem repozytorium **`mdz-hub/weatherApp`** bezpośrednio w kodzie. To ważne, bo README praktycznie nie istnieje, a projekt nie jest klasyczną aplikacją webową typu React/Next/Vite.

 Repozytorium weatherApp na GitHub

 ## 1\. Do czego służy aplikacja?

 To **Pythonowy proces zbierający dane pogodowe**.

 Schemat działania jest mniej więcej taki:

```
OpenWeatherMap API
        │
        ▼
   openweather_api.py
        │
        ├── temperatura
        ├── temperatura odczuwalna
        ├── wilgotność
        ├── ciśnienie
        ├── wiatr
        ├── zachmurzenie
        ├── miasto
        └── godzina wschodu słońca
        │
        ├───────────────┐
        ▼               ▼
    weather.xlsx      MySQL
                        │
                        ▼
                    tabela records
```

 `main.py` uruchamia pobieranie danych, zapisuje wynik do Excela oraz do bazy MySQL, po czym czeka **120 sekund** i wykonuje cały cykl ponownie.  GitHub+2

 Czyli aplikacja jest bardziej **kolektorem danych pogodowych / ETL-em** niż aplikacją pogodową dla użytkownika.

---

 # 2\. Co dokładnie pobiera?

 W `services/openweather_api.py` znajduje się zapytanie:

```
https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={KEY}
```

 A więc aplikacja korzysta z **OpenWeatherMap Current Weather API** i pobiera pogodę dla miasta określonego w `.env`.  GitHub+1

 Z odpowiedzi API wyciągane są:

 | Pole | Znaczenie |
| --- | --- |
| `temp` | temperatura °C |
| `feels_like` | temperatura odczuwalna °C |
| `humidity` | wilgotność % |
| `pressure` | ciśnienie hPa |
| `wind` | prędkość wiatru |
| `clouds` | zachmurzenie % |
| `city` | nazwa miasta |
| `sunrise` | godzina wschodu słońca |
| `timestamp` | moment wykonania pomiaru |

 GitHub  OpenWeather domyślnie zwraca temperaturę w Kelvinach, dlatego kod sam przelicza ją na °C.  openweathermap.org+1

---

 # 3\. Struktura repozytorium

 Obecnie repo wygląda tak:

```
weatherApp/
│
├── common/
│   └── functions.py
│
├── services/
│   ├── openweather_api.py
│   ├── mysql_db.py
│   ├── files.py
│   └── dashboard.py
│
├── config.py
└── main.py
```

 GitHub pokazuje obecnie tylko kilka plików i zaledwie dwa commity.  GitHub

 ### `config.py`

 To centralna konfiguracja.

 Kod odczytuje z `.env`:

```
OW_API_KEY = os.getenv("ENV_OW_API_KEY")
OW_CITY = os.getenv("ENV_OW_CITY")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
```

 oraz ustala nazwę pliku:

```
EXCEL_FILEPATH = "weather.xlsx"
```

  GitHub
---

 # 4\. Co trzeba zainstalować?

 Repozytorium **nie zawiera `requirements.txt`**, więc zależności trzeba ustalić na podstawie importów w kodzie.

 Potrzebujesz:

 - Python
- `requests`
- `python-dotenv`
- `pandas`
- `openpyxl`
- `mysql-connector-python`
- `streamlit` — tylko jeśli chcesz korzystać z dashboardu

 Najprościej:

```
pip install requests python-dotenv pandas openpyxl mysql-connector-python streamlit
```

 `mysql-connector-python` jest oficjalnym konektorem MySQL dla Pythona i można go instalować przez `pip`.  GitHub

 Ja dodatkowo zrobiłbym virtual environment:

```
python -m venv .venv
```

 Windows:

```
.venv\Scripts\activate
```

 Linux/macOS:

```
source .venv/bin/activate
```

 Następnie:

```
pip install requests python-dotenv pandas openpyxl mysql-connector-python streamlit
```

---

 # 5\. Jak stworzyć `.env`?

 W katalogu głównym projektu:

```
weatherApp/
├── .env
├── main.py
├── config.py
├── common/
└── services/
```

 Tworzysz:

```
.env
```

 I wpisujesz:

```
ENV_OW_API_KEY=TU_WKLEJ_KLUCZ_OPENWEATHER
ENV_OW_CITY=Warsaw

DB_HOST=localhost
DB_USER=weather_user
DB_PASSWORD=twoje_haslo
DB_NAME=weather
```

 ### Czyli wszystkie zmienne:

 | Zmienna | Wartość | Do czego |
| --- | --- | --- |
| `ENV_OW_API_KEY` | API key | OpenWeatherMap |
| `ENV_OW_CITY` | np. `Warsaw` | miasto, dla którego pobieramy pogodę |
| `DB_HOST` | np. `localhost` | adres MySQL |
| `DB_USER` | np. `weather_user` | użytkownik MySQL |
| `DB_PASSWORD` | np. `secret123` | hasło MySQL |
| `DB_NAME` | np. `weather` | baza danych |

Klucz OpenWeather można wygenerować po założeniu konta w OpenWeather.  openweathermap.org

 OpenWeather – strona API / generowanie klucza

 **Uwaga:** nazwy zmiennych muszą być dokładnie takie jak powyżej. Kod nie szuka np. `OPENWEATHER_API_KEY`, tylko konkretnie `ENV_OW_API_KEY`.  GitHub

---

 # 6\. MySQL — trzeba mieć bazę

 To jest ważne: sama instalacja `mysql-connector-python` nie wystarczy.

 Potrzebujesz działającego **serwera MySQL**.

 Przykładowo możesz stworzyć bazę:

```
CREATE DATABASE weather;
```

 oraz użytkownika:

```
CREATE USER 'weather_user'@'localhost'
IDENTIFIED BY 'twoje_haslo';

GRANT ALL PRIVILEGES ON weather.*
TO 'weather_user'@'localhost';

FLUSH PRIVILEGES;
```

 Wtedy `.env`:

```
DB_HOST=localhost
DB_USER=weather_user
DB_PASSWORD=twoje_haslo
DB_NAME=weather
```

 Program sam próbuje stworzyć tabelę `records`.  GitHub

---

 # 7\. Co znajduje się w bazie?

 `mysql_db.py` tworzy tabelę:

```
CREATE TABLE IF NOT EXISTS records (
    id CHAR(36) PRIMARY KEY DEFAULT(UUID()),
    temp FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    humidity INT NOT NULL,
    pressure INT NOT NULL,
    wind FLOAT NOT NULL,
    clouds INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    sunrise TIME NOT NULL,
    timestamp DATETIME NOT NULL
);
```

  GitHub  Czyli po pewnym czasie możesz mieć np.:

```
id                                   temp   humidity   city      timestamp
--------------------------------------------------------------------------------
...                                  14.5   72         Warsaw    2026-10-03 13:00:00
...                                  14.8   70         Warsaw    2026-10-03 13:02:00
...                                  15.1   69         Warsaw    2026-10-03 13:04:00
```

 Ponieważ pomiar wykonywany jest co 120 sekund, baza może z czasem zebrać całkiem spory zbiór danych.

---

 # 8\. Excel

 Oprócz MySQL dane są zapisywane do:

```
weather.xlsx
```

 Kod sprawdza, czy plik istnieje.

 Jeśli nie:

```
weather.xlsx
```

 jest tworzony.

 Jeżeli istnieje, program odczytuje jego zawartość, dopisuje nowy rekord i zapisuje plik ponownie.  GitHub

 Do tego potrzebne są:

```
pip install pandas openpyxl
```

---

 # 9\. Dashboard Streamlit

 W projekcie jest również:

```
services/dashboard.py
```

 To jest próba zrobienia prostego dashboardu w **Streamlit**.

 Dashboard pokazuje m.in.:

 - temperaturę,
- temperaturę odczuwalną,
- wiatr,
- wilgotność,
- ciśnienie,
- zachmurzenie,
- tabelę pomiarów,
- wykres temperatury,
- wykres temperatury odczuwalnej,
- wykres wilgotności.

  GitHub  Przykładowo:

```
st.metric("Temperatura", f"{temp}°C")
```

 oraz:

```
st.line_chart(temp_chart)
```

  GitHub  ### Ale jest tutaj problem

 W `main.py`:

```
# Wyświetlanie dashboardu
# render()
```

 czyli dashboard jest **zakomentowany**.  GitHub

 Co więcej, `dashboard.py` oczekuje pliku:

```
FILE = "weather_2026_350.csv"
```

 podczas gdy główny program zapisuje:

```
weather.xlsx
```

 To oznacza, że dashboard w obecnej postaci **nie jest spójny z resztą aplikacji**.  GitHub+1

---

 # 10\. Jak uruchomić projekt?

 Po instalacji:

```
git clone https://github.com/mdz-hub/weatherApp.git
cd weatherApp
```

 Utwórz virtualenv:

```
python -m venv .venv
```

 Aktywuj:

```
# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

 Zainstaluj:

```
pip install requests python-dotenv pandas openpyxl mysql-connector-python streamlit
```

 Stwórz `.env`:

```
ENV_OW_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ENV_OW_CITY=Warsaw

DB_HOST=localhost
DB_USER=weather_user
DB_PASSWORD=twoje_haslo
DB_NAME=weather
```

 Uruchom:

```
python main.py
```

---

 # 11\. Co się wtedy dzieje?

 `main.py` robi:

```
create_weather_table()

while True:
    weather = get_weather()
    create_file([weather])
    save_weather(weather)

    print("Pobrałem dane")

    time.sleep(120)
```

  GitHub  Czyli:

```
START
  │
  ▼
połącz z MySQL
  │
  ▼
utwórz records jeśli nie istnieje
  │
  ▼
pobierz pogodę z OpenWeather
  │
  ▼
zapisz do weather.xlsx
  │
  ▼
zapisz do MySQL
  │
  ▼
czekaj 120 sekund
  │
  └──────────────► powtórz
```

 To jest więc **proces działający w nieskończonej pętli**.

---

 # 12\. Jest jednak kilka problemów w obecnym kodzie

 I tutaj repozytorium wymaga trochę ostrożności — **nie traktowałbym go jako projektu gotowego do uruchomienia bez poprawek**.

 ### Problem 1 — potencjalny błąd przy pierwszym uruchomieniu

 W `mysql_db.py` na samym dole znajduje się:

```
odczytane = get_all_records()

print(odczytane[-1])
```

  GitHub  A `main.py` importuje wcześniej:

```
from services.mysql_db import create_weather_table, save_weather
```

 Dopiero później wykonuje:

```
create_weather_table()
```

  GitHub  Czyli kolejność może być:

```
import mysql_db
      ↓
get_all_records()
      ↓
SELECT * FROM records
      ↓
records jeszcze nie istnieje
      ↓
błąd
```

 i następnie:

```
print(odczytane[-1])
```

 może spowodować kolejny problem, ponieważ `get_all_records()` w przypadku błędu zwraca `None`.

 **To jest realny bug, który poprawiłbym przed pierwszym uruchomieniem.**

---

 ### Problem 2 — błędne przeliczenie prędkości wiatru

 W `common/functions.py` jest:

```
from_ms_to_kmh = lambda s: round(s * 3.6 / 2)
```

  GitHub  A poprawne przeliczenie:

```
1 m/s = 3.6 km/h
```

 więc powinno być:

```
round(s * 3.6, 2)
```

 Obecny kod w praktyce dzieli wynik przez 2.

 Czyli np.:

```
10 m/s
```

 powinno być:

```
36 km/h
```

 a obecny kod daje około:

```
18 km/h
```

---

 ### Problem 3 — brak obsługi HTTP statusów

 Kod robi:

```
response = requests.get(URL)
data = response.json()
```

 ale nie robi:

```
response.raise_for_status()
```

  GitHub  Jeżeli API zwróci np. błąd 401 z powodu złego klucza albo 404 dla nieprawidłowego miasta, aplikacja może dostać JSON błędu i potem wywalić się na:

```
data.get("main").get("temp")
```

 Lepsze byłoby:

```
response.raise_for_status()
```

 plus sensowna obsługa błędów.

---

 ### Problem 4 — brak timeoutu

 Jest:

```
requests.get(URL)
```

 Bez timeoutu.

 Bezpieczniej:

```
requests.get(URL, timeout=10)
```

---

 ### Problem 5 — `get_weather2()` wygląda na niedokończoną funkcję

 W kodzie jest druga funkcja:

```
def get_weather2():
```

 która próbuje korzystać z:

```
App.OW_CITY2
```

 ale `config.py` nie definiuje `OW_CITY2`.  GitHub+1

 Wygląda to na pozostałość po próbie obsługi drugiego miasta.

---

 ### Problem 6 — dashboard jest niespójny z kolektorem

 Collector zapisuje:

```
weather.xlsx
```

 a dashboard próbuje czytać:

```
weather_2026_350.csv
```

  GitHub+1  Czyli obecnie te dwie części projektu nie tworzą jednego kompletnego przepływu.

---

 # 13\. Minimalna konfiguracja, którą bym zrobił

 Jeśli Twoim celem jest **po prostu odpalić projekt**, potrzebujesz:

```
Python
MySQL
OpenWeather API key
```

 i:

```
pip install requests python-dotenv pandas openpyxl mysql-connector-python
```

 `.env`:

```
ENV_OW_API_KEY=TWÓJ_KLUCZ
ENV_OW_CITY=Warsaw

DB_HOST=localhost
DB_USER=weather_user
DB_PASSWORD=twoje_haslo
DB_NAME=weather
```

 Następnie:

```
python main.py
```

 Dane będą trafiały do:

```
weather.xlsx
```

 oraz:

```
MySQL → weather → records
```

---

 # 14\. Jak ja bym ocenił architekturę projektu

 Aktualnie jest to raczej **prosty projekt edukacyjny / prototyp ETL**:

```
             ┌──────────────────────┐
             │    OpenWeatherMap    │
             └──────────┬───────────┘
                        │
                        ▼
             ┌──────────────────────┐
             │ openweather_api.py   │
             └──────────┬───────────┘
                        │
                  weather dict
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
      ┌──────────────┐     ┌──────────────┐
      │    Excel     │     │    MySQL     │
      │ weather.xlsx │     │   records    │
      └──────────────┘     └──────────────┘
```

 Do tego jest rozpoczęty:

```
MySQL/Excel
     │
     ▼
Streamlit Dashboard
```

 ale ta część nie jest obecnie spięta poprawnie z resztą aplikacji.

---

 ## Najważniejsza rzecz

 Jeżeli Twoim celem jest **uruchomienie tego repo lokalnie**, nie zaczynałbym od Streamlit. Najpierw:

 1. zainstalować Python,
2. zainstalować zależności,
3. uruchomić MySQL,
4. stworzyć bazę `weather`,
5. stworzyć `.env`,
6. poprawić błąd w `mysql_db.py`,
7. poprawić przeliczanie wiatru,
8. odpalić `python main.py`,
9. sprawdzić `weather.xlsx` i tabelę `records`.

 Dopiero później podłączałbym dashboard.

 **Warto też zauważyć, że repo nie zawiera `requirements.txt`, `.env.example` ani README opisującego instalację**, więc dokumentacja uruchomieniowa, którą podałem wyżej, jest rekonstrukcją na podstawie faktycznych importów i kodu projektu, a nie instrukcją dostarczoną przez autora.  GitHub
