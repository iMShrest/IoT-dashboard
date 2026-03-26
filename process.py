import pandas as pd

df = pd.read_csv("data.csv")

print("\n--- Summary ---")
print("Average Temperature:", df["temperature"].mean())
print("Average Humidity:", df["humidity"].mean())
print("Average AQI:", df["aqi"].mean())

# Simple AQI classification
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive"
    else:
        return "Unhealthy"

df["aqi_status"] = df["aqi"].apply(classify_aqi)

print("\nSample Data:")
print(df.head())