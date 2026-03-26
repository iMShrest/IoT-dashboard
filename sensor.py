import random
import time
import csv

def generate_data():
    temperature = round(random.uniform(20, 35), 2)
    humidity = round(random.uniform(30, 80), 2)
    aqi = random.randint(50, 200)
    return temperature, humidity, aqi

with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "temperature", "humidity", "aqi"])

    for i in range(50):  # simulate 50 readings
        t, h, a = generate_data()
        writer.writerow([time.time(), t, h, a])
        print(f"Generated: Temp={t}, Hum={h}, AQI={a}")
        time.sleep(1)