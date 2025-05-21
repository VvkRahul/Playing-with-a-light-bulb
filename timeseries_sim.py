import time
import random
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def simulate_bulb_reading():
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    state = "ON" if random.random() > 0.4 else "OFF"
    brightness = random.randint(20, 100) if state == "ON" else 0
    power = round(brightness * 0.1, 2) if state == "ON" else 0.0
    return {
        "timestamp": timestamp,
        "state": state,
        "brightness": brightness,
        "power": power
    }

log = []
for _ in range(10):
    log.append(simulate_bulb_reading())
    time.sleep(1)

df = pd.DataFrame(log)

plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["brightness"], label="Brightness (%)", marker='o')
plt.plot(df["timestamp"], df["power"], label="Power (W)", marker='s')
plt.xticks(rotation=45)
plt.title("Time-Series Bulb Sensor Data")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
