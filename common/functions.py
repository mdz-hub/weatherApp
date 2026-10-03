from datetime import datetime

# Funkcja przeliczania milisekundy na format godzina:minuta:sekunda
from_ts = lambda x: datetime.fromtimestamp(x).strftime("%H:%M:%S")

# Funkcja przeliczająca Kelwiny na stopnie Celsjusza, zaokrąglająca do dwóch miejsc po przecinku
from_kel_to_cel = lambda t: round (t - 273.15, 2)

# Funkcja przeliczająca m/s na km/h, zaokrąglająca do dwóch miejsc po przecinku
from_ms_to_kmh = lambda s: round (s* 3.6/2)