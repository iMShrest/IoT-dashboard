import sqlite3

conn = sqlite3.connect("iot.db")
cursor = conn.cursor()

cursor.execute("""e
CREATE TABLE IF NOT EXISTS sensor_data (
    time REAL,
    temperature REAL,
    humidity REAL,
    aqi INTEGER
)
""")

conn.commit()
conn.close()