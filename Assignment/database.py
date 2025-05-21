import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="bulb_data.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bulb_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                name TEXT,
                status TEXT,
                brightness INTEGER,
                power REAL,
                time_elapsed INTEGER,
                timestamp TEXT
            )
        """)
        self.conn.commit()

        self.cursor.execute("PRAGMA table_info(bulb_log)")
        columns = [col[1] for col in self.cursor.fetchall()]
        if "session_id" not in columns:
            print("🛠️ Adding missing 'session_id' column...")
            self.cursor.execute("ALTER TABLE bulb_log ADD COLUMN session_id TEXT")
            self.conn.commit()

    def insert_data(self, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO bulb_log (session_id, name, status, brightness, power, time_elapsed, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data["session_id"], data["name"], data["status"], data["brightness"],
              data["power"], data["time_elapsed"], timestamp))
        self.conn.commit()

    def close(self):
        self.conn.close()
