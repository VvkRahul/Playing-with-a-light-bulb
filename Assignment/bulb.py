class Bulb:
    def __init__(self, name="Bulb"):
        self.name = name
        self.status = "OFF"
        self.brightness = 0
        self.time_elapsed = 0

    def set_state(self, status, brightness):
        self.status = status
        self.brightness = brightness if status == "ON" else 0

    def get_current_data(self):
        power = round(self.brightness / 10, 2) if self.status == "ON" else 0
        return {
            "name": self.name,
            "status": self.status,
            "brightness": self.brightness,
            "power": power,
            "time_elapsed": self.time_elapsed
        }

    def tick(self):
        self.time_elapsed += 1
