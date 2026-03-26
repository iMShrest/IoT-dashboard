import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

plt.figure()
plt.plot(df["temperature"])
plt.title("Temperature Over Time")
plt.xlabel("Reading")
plt.ylabel("Temperature")
plt.show()

plt.figure()
plt.plot(df["aqi"])
plt.title("AQI Over Time")
plt.xlabel("Reading")
plt.ylabel("AQI")
plt.show()