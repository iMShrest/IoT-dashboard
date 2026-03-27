import paho.mqtt.client as mqtt
import sqlite3
import json

broker = "broker.hivemq.com"
topic = "iot/sensor/data"

conn = sqlite3.connect("iot.db", check_same_thread=False)
conn.execute("PRAGMA journal_mode=WAL;")
cursor = conn.cursor()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    cursor.execute(
        "INSERT INTO sensor_data VALUES (?, ?, ?, ?)",
        (data["time"], data["temperature"], data["humidity"], data["aqi"])
    )
    conn.commit()

    print("Saved:", data)

client = mqtt.Client()
client.connect(broker, 1883, 60)

client.subscribe(topic)
client.on_message = on_message

print("Listening for IoT data...")

client.loop_forever()