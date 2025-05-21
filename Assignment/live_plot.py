import sqlite3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def fetch_data():
    conn = sqlite3.connect("bulb_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time_elapsed, brightness FROM bulb_log ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return list(reversed(rows))  # To plot in ascending time

def animate(i):
    data = fetch_data()
    if not data:
        return

    times = [row[0] for row in data]
    brightness = [row[1] for row in data]

    ax.clear()
    ax.plot(times, brightness, marker='o', color='orange')
    ax.set_title("Real-Time Bulb Brightness")  # Removed 💡 to avoid font warning
    ax.set_xlabel("Time Elapsed (s)")
    ax.set_ylabel("Brightness (%)")
    ax.grid(True)
    plt.tight_layout()

# Plot setup
fig, ax = plt.subplots()
ani = FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)  # Cleaned
plt.show()
