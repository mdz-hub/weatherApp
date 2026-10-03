import streamlit as st
import pandas as pd


def render():
    FILE = "weather_2026_350.csv"
    df = pd.read_csv(FILE)

    st.set_page_config(
        page_title="Aplikacja Pogodowa",
        layout="wide",
    )

    st.sidebar.header("Konfiguracja")

    # Wybór ilości widocznych wierszy
    rows_limit = st.sidebar.slider(
        "Ilość rekordów w tabeli",
        min_value=1,
        max_value=df.shape[0],
        value=10,
        step=10
    )

    extra_metric = st.sidebar.selectbox(
        "Dodatkowa informacja",
        ["clouds", "humidity", "pressure"]
    )

    # ---------------------------------------------------------------
    st.title("Aplikacja Pogodowa")
    st.write("Dane pogodowe dla wybranego miasta, pochodzące z OpenWeatherAPI")

    # Informacje o najnowszym rekordzie pogodowym
    last_row = df.iloc[-1]   # najnowsze zapisują się ostatnie

    st.subheader("Aktualna pogoda")
    upper_cols = st.columns(4)  # tworzy cztery kolumny
    with upper_cols[0]:
        temp = last_row.get("temp")
        upper_cols[0].metric("Temperatura", f"{temp}°C")
    with upper_cols[1]:
        feels_like = last_row.get("feels_like")
        upper_cols[1].metric("Odczuwalna", f"{feels_like}°C")
    with upper_cols[2]:
        wind_speed = last_row.get("wind")
        upper_cols[2].metric("Wiatr", f"{wind_speed}km/h")
    with upper_cols[3]:
        metric_value = last_row.get(extra_metric)
        upper_cols[3].metric(extra_metric.title(), metric_value)

    # Tabela z danymi
    st.divider()
    st.subheader("Zapisane odczyty")
    st.write("Odczyty pogodowe w roku 2026")

    st.dataframe(
        df.head(rows_limit)
    )

 # Wykresy liniowe
    st.subheader("Temperatura w czasie")

    temp_chart = df.set_index("timestamp")[["temp","feels_like"]]
    st.line_chart(temp_chart, use_container_width=True)

    # Wilgotność
    humidity_chart = df.set_index("timestamp")[["humidity"]]

    st.line_chart(humidity_chart, use_container_width=True)