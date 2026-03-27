import paho.mqtt.client as mqtt
import random
import time
import json

broker = "broker.hivemq.com"
topic = "iot/sensor/data"

client = mqtt.Client()
client.connect(broker, 1883, 60)

def generate_data():
    return {
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 80), 2),
        "aqi": random.randint(50, 200),
        "time": time.time()
    }

while True:
    data = generate_data()
    client.publish(topic, json.dumps(data))
    print("Published:", data)
    time.sleep(2)