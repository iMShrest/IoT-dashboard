import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Settings")
refresh_interval = st.sidebar.slider("Refresh rate (sec)", 1, 10, 2)
limit = st.sidebar.slider("Max data points", 10, 200, 50)

# ---------- AQI STATUS ----------
def get_aqi_status(aqi):
    if aqi <= 50:
        return "🟢 Good", "green"
    elif aqi <= 100:
        return "🟡 Moderate", "orange"
    else:
        return "🔴 Unhealthy", "red"

# ---------- HEADER ----------
st.title("🌍 IoT Environmental Monitoring Dashboard")

# ---------- REFRESH BUTTON ----------
if st.button("🔄 Refresh Now"):
    st.rerun()

placeholder = st.empty()

# ---------- MAIN LOOP ----------
while True:
try:
    df = pd.read_csv("data.csv")
    df = df.tail(limit)

    latest = df.iloc[-1]
    status, color = get_aqi_status(latest["aqi"])

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature", f"{latest['temperature']} °C")
    col2.metric("💧 Humidity", f"{latest['humidity']} %")
    col3.metric("🌫️ AQI", f"{latest['aqi']}")

    st.markdown(f"### AQI Status: <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)

    st.line_chart(df["temperature"])
    st.line_chart(df["humidity"])
    st.line_chart(df["aqi"])

except:
    st.warning("No data available yet!")

    time.sleep(refresh_interval)