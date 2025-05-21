import time
from bulb import Bulb
from database import Database

def run_simulation(duration=20):
    bulb = Bulb("SmartBulb")
    db = Database()

    print(f"💡 Starting simulation for {bulb.name}...\n")

    for _ in range(duration):
        bulb.tick()
        data = bulb.get_current_data()
        print(f"[{data['time_elapsed']}s] State: {data['status']}, Brightness: {data['brightness']}%, Power: {data['power']}W")
        db.insert_data(data)
        time.sleep(1)

    db.close()
    print("\n✅ Simulation complete. Data saved to database.")

if __name__ == "__main__":
    run_simulation()
