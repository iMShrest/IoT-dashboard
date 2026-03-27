import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="IoT Dashboard", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox("Select Mode", ["Simulator", "Live API"])
limit = st.sidebar.slider("Max data points", 10, 200, 50)

# Location for API
locations = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "London": (51.5074, -0.1278)
}
selected_city = st.sidebar.selectbox("Location", list(locations.keys()))
lat, lon = locations[selected_city]

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

# Refresh button
if st.button("🔄 Refresh"):
    st.rerun()

# ==============================
# MODE 1: SIMULATOR
# ==============================
if mode == "Simulator":
    st.subheader("📡 Simulator Mode")

    try:
        df = pd.read_csv("data.csv")
        df = df.tail(limit)

        latest = df.iloc[-1]
        status, color = get_aqi_status(latest["aqi"])

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{latest['temperature']} °C")
        col2.metric("💧 Humidity", f"{latest['humidity']} %")
        col3.metric("🌫️ AQI", f"{latest['aqi']}")

        st.markdown(
            f"### AQI Status: <span style='color:{color}'>{status}</span>",
            unsafe_allow_html=True
        )

        st.line_chart(df["temperature"])
        st.line_chart(df["humidity"])
        st.line_chart(df["aqi"])

    except:
        st.warning("Run sensor.py to generate data.")

# ==============================
# MODE 2: LIVE API
# ==============================
elif mode == "Live API":
    st.subheader("🌐 Live API Mode")

    try:
        url = f"https://api.openaq.org/v2/latest?coordinates={lat},{lon}&radius=10000"
        response = requests.get(url).json()

        if "results" not in response or len(response["results"]) == 0:
            st.warning("No data found for this location.")
        else:
            measurements = response["results"][0].get("measurements", [])

            data = {}
            for m in measurements:
                data[m["parameter"]] = m["value"]

            pm25 = data.get("pm25", None)

            if pm25 is None:
                st.warning("PM2.5 not available.")
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