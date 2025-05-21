import tkinter as tk
from tkinter import Canvas
from database import Database
import time
import uuid

class BulbControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Bulb Controller")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.db = Database()
        self.session_id = str(uuid.uuid4())
        print("🆕 Session ID:", self.session_id)

        self.status = "OFF"
        self.brightness_level = 0

        self.canvas = Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.pack(pady=20)
        self.bulb = self.canvas.create_oval(100, 50, 200, 150, fill="gray")

        self.toggle_button = tk.Button(self.root, text="Toggle Power", command=self.toggle_power)
        self.toggle_button.pack(pady=10)

        self.brightness_button = tk.Button(self.root, text="Increase Brightness", command=self.change_brightness)
        self.brightness_button.pack(pady=10)

        self.info_label = tk.Label(self.root, text="Status: OFF | Brightness: 0")
        self.info_label.pack(pady=10)

    def toggle_power(self):
        if self.status == "OFF":
            self.status = "ON"
            if self.brightness_level == 0:
                self.brightness_level = 1
        else:
            self.status = "OFF"
            self.brightness_level = 0
        self.update_bulb()
        self.log_to_db()

    def change_brightness(self):
        if self.status == "ON":
            self.brightness_level = self.brightness_level + 1 if self.brightness_level < 5 else 1
            self.update_bulb()
            self.log_to_db()

    def update_bulb(self):
        brightness_color = {
            0: "gray",
            1: "#FFD580",
            2: "#FFC04D",
            3: "#FFB733",
            4: "#FFA500",
            5: "#FF8C00"
        }
        self.canvas.itemconfig(self.bulb, fill=brightness_color[self.brightness_level])
        self.info_label.config(text=f"Status: {self.status} | Brightness: {self.brightness_level}")

    def log_to_db(self):
        power = round((self.brightness_level * 20) * 0.1, 2) if self.status == "ON" else 0.0
        brightness = self.brightness_level * 20 if self.status == "ON" else 0
        data = {
            "session_id": self.session_id,
            "name": "SmartBulb",
            "status": self.status,
            "brightness": brightness,
            "power": power,
            "time_elapsed": int(time.time())
        }
        self.db.insert_data(data)

    def on_close(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BulbControlApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
