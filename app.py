from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    session_id = request.args.get("session_id")

    conn = sqlite3.connect("bulb_data.db")
    cursor = conn.cursor()

    if not session_id:
        cursor.execute("SELECT session_id FROM bulb_log WHERE session_id IS NOT NULL ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        session_id = result[0] if result else None

    if session_id:
        cursor.execute("""
            SELECT name, status, brightness, power, time_elapsed, timestamp
            FROM bulb_log WHERE session_id = ?
        """, (session_id,))
    else:
        return jsonify([])

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "name": row[0],
            "status": row[1],
            "brightness": row[2],
            "power": row[3],
            "time_elapsed": row[4],
            "timestamp": row[5],
        }
        for row in rows
    ])

@app.route("/api/sessions")
def get_sessions():
    conn = sqlite3.connect("bulb_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, MIN(timestamp), MAX(timestamp), COUNT(*) 
        FROM bulb_log
        WHERE session_id IS NOT NULL
        GROUP BY session_id
        ORDER BY MAX(timestamp) DESC
    """)
    sessions = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "session_id": row[0],
            "start_time": row[1],
            "end_time": row[2],
            "entries": row[3]
        } for row in sessions
    ])

if __name__ == "__main__":
    app.run(debug=True)
