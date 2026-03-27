import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# Sidebar
st.sidebar.title("⚙️ Settings")
city = st.sidebar.selectbox("City", ["Delhi", "Mumbai", "Kolkata", "London"])

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

    # Check if results exist
    if "results" not in response or len(response["results"]) == 0:
        st.warning("No data found for this city. Try another one.")
    else:
        measurements = response["results"][0].get("measurements", [])

        data = {}
        for m in measurements:
            data[m["parameter"]] = m["value"]

        pm25 = data.get("pm25", None)

        if pm25 is None:
            st.warning("PM2.5 data not available for this location.")
        else:
            status, color = get_aqi_status(pm25)

            col1, col2, col3 = st.columns(3)
            col1.metric("🌡️ Temperature", data.get("temperature", "N/A"))
            col2.metric("💧 Humidity", data.get("humidity", "N/A"))
            col3.metric("🌫️ PM2.5", pm25)

            st.markdown(
                f"### AQI Status: <span style='color:{color}'>{status}</span>",
                unsafe_allow_html=True
            )

except Exception as e:
    st.error(f"API Error: {e}")