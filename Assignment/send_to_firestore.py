import sqlite3
import firebase_admin
from firebase_admin import credentials, firestore
import time

# 🔐 Initialize Firebase
cred = credentials.Certificate("your-firebase-creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🌟 Get document count to start from next index
def get_next_doc_number():
    docs = db.collection("bulb_logs").stream()
    return sum(1 for _ in docs) + 1

# 📦 Get latest entry from SQLite
def fetch_latest_data():
    conn = sqlite3.connect("bulb_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bulb_log ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        id, time_elapsed, status, brightness, power = row
        return id, {
            "time_elapsed": time_elapsed,
            "status": status,
            "brightness": brightness,
            "power": power
        }
    return None, None

# 🔁 Monitor for new entries
def monitor_and_push():
    last_uploaded_id = -1  # Start with -1 (nothing uploaded)

    while True:
        latest_id, latest_data = fetch_latest_data()
        if latest_id is not None and latest_id != last_uploaded_id:
            doc_name = f"new_data_{get_next_doc_number()}"
            db.collection("bulb_logs").document(doc_name).set(latest_data)
            print(f"✅ Uploaded: {doc_name} -> {latest_data}")
            last_uploaded_id = latest_id
        time.sleep(1)  # Poll every second

if __name__ == "__main__":
    monitor_and_push()
