import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Settings")
city = st.sidebar.text_input("City", "Delhi")

def get_aqi_status(aqi):
    if aqi <= 50:
        return "🟢 Good", "green"
    elif aqi <= 100:
        return "🟡 Moderate", "orange"
    else:
        return "🔴 Unhealthy", "red"

st.title("🌍 Live Air Quality Dashboard")

if st.button("🔄 Refresh"):
    st.rerun()

try:
    url = f"https://api.openaq.org/v2/latest?city={city}"
    response = requests.get(url).json()

    measurements = response["results"][0]["measurements"]

    data = {}
    for m in measurements:
        data[m["parameter"]] = m["value"]

    # Extract values safely
    temperature = data.get("temperature", "N/A")
    humidity = data.get("humidity", "N/A")
    pm25 = data.get("pm25", 0)

    status, color = get_aqi_status(pm25)

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature", temperature)
    col2.metric("💧 Humidity", humidity)
    col3.metric("🌫️ PM2.5 (AQI Proxy)", pm25)

    st.markdown(f"### AQI Status: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

except Exception as e:
    st.error("Error fetching data. Try another city.")