import random
import math
import time
import sqlite3

conn = sqlite3.connect("iot.db", check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL;")
cursor = conn.cursor()

def generate_data():
    temperature = round(random.uniform(20, 35), 2)
    humidity = round(random.uniform(30, 80), 2)
    aqi = int(80 + 40 * math.sin(time.time()))
    return temperature, humidity, aqi

while True:
    t, h, a = generate_data()

    cursor.execute(
        "INSERT INTO sensor_data VALUES (?, ?, ?, ?)",
        (time.time(), t, h, a)
    )

    conn.commit()

    print(f"Temp={t}, Hum={h}, AQI={a}")
    time.sleep(2)