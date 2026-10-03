import mysql.connector as sql
from config import App

# Funkcja tworząca połączenie z baza danych
def get_connnection():
    return sql.connect(
        host = App.DB_HOST,
        user = App.DB_USER,
        password = App.DB_PASSWORD,
        database = App.DB_NAME,
    )

def create_weather_table():
    query = """
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
    timestamp DATETIME NOT NULL);
    """

    try:
        connection = get_connnection()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabela została utworzona lub już istnieje")

    except Exception as e:
        print(e)

def save_weather(data):
    insert = """
    INSERT INTO records 
    (temp,feels_like,humidity,pressure,wind,clouds,city,sunrise,timestamp)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    values = (
        data['temp'],
        data['feels_like'],
        data['humidity'],
        data['pressure'],
        data['wind'],
        data['clouds'],
        data['city'],
        data['sunrise'],
        data['timestamp']
    )
    try:
        connection = get_connnection()
        cursor = connection.cursor()
        cursor.execute(insert, values)
        connection.commit()
        print("Informacja zapisana w bazie MySQL")
    except Exception as e:
        print(e)


# funkcjonalność opcjonalna zapisu odczytu pogody
def get_all_records():
    query = "SELECT * FROM records"

    try:
        connection = get_connnection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as err:
        print(err)


odczytane = get_all_records()
# najnowszy odczyt
print(odczytane[-1])
