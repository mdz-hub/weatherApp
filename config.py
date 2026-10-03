from dotenv import load_dotenv
import os
load_dotenv()

class App:
    OW_API_KEY = os.getenv("ENV_OW_API_KEY")
    OW_CITY = os.getenv("ENV_OW_CITY")
    EXCEL_FILEPATH = "weather.xlsx"
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
