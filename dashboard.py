import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# ---------- CUSTOM STYLE ----------
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🌍 Smart Environmental Monitoring System")
st.caption("Real-time IoT + Cloud Dashboard")

# ---------- SIDEBAR ----------
mode = st.sidebar.selectbox("Mode", ["Simulator", "Live API"])

# ---------- AQI STATUS ----------
def get_status(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Moderate"
    else:
        return "🔴 Unhealthy"

# ---------- SIMULATOR ----------
if mode == "Simulator":
    try:
        df = pd.read_csv("data.csv").tail(50)
        latest = df.iloc[-1]

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='metric-card'>🌡️<br>{latest['temperature']} °C</div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric-card'>💧<br>{latest['humidity']} %</div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric-card'>🌫️<br>{latest['aqi']}</div>", unsafe_allow_html=True)

        st.markdown(f"### Air Quality: {get_status(latest['aqi'])}")

        st.markdown("## 📊 Trends")

        col4, col5 = st.columns(2)

        col4.area_chart(df[["temperature", "humidity"]])
        col5.line_chart(df["aqi"])

    except:
        st.warning("Run sensor.py first")

# ---------- API ----------
else:
    try:
        url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=28.6&longitude=77.2&current=pm2_5"
        res = requests.get(url).json()

        pm25 = res["current"]["pm2_5"]

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temp", "N/A")
        col2.metric("💧 Humidity", "N/A")
        col3.metric("🌫️ PM2.5", pm25)

        st.markdown(f"### Air Quality: {get_status(pm25)}")

    except:
        st.error("API failed")