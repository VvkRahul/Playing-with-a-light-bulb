// src/App.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [data, setData] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [lastUpdated, setLastUpdated] = useState("");

  // Fetch session list
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/sessions");
        setSessions(res.data);
        if (!selectedSession && res.data.length > 0) {
          setSelectedSession(res.data[0].session_id);
        }
      } catch (err) {
        console.error("Error fetching sessions:", err);
      }
    };

    fetchSessions();
  }, [selectedSession]);

  // Fetch data for selected session
  useEffect(() => {
    if (!selectedSession) return;

    const fetchData = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/data", {
          params: { session_id: selectedSession },
        });
        setData(res.data);
        setLastUpdated(new Date().toLocaleTimeString());
      } catch (err) {
        console.error("Error fetching data:", err);
      }
    };

    fetchData(); // initial
    const interval = setInterval(fetchData, 2000); // polling
    return () => clearInterval(interval);
  }, [selectedSession]);

  return (
    <div className="App">
      <h1>💡 Smart Bulb Dashboard</h1>
      <div className="controls">
        <label>Session:</label>
        <select
          value={selectedSession}
          onChange={(e) => setSelectedSession(e.target.value)}
        >
          {sessions.map((s) => (
            <option key={s.session_id} value={s.session_id}>
              {s.start_time} ({s.entries} logs)
            </option>
          ))}
        </select>
        <p className="last-updated">Last updated: {lastUpdated}</p>
      </div>
      <table>
        <thead>
          <tr>
            <th>Time</th>
            <th>State</th>
            <th>Brightness</th>
            <th>Power (W)</th>
          </tr>
        </thead>
        <tbody>
          {data.map((entry, index) => (
            <tr key={index}>
              <td>{entry.timestamp}</td>
              <td className={entry.status === "ON" ? "on" : "off"}>
                {entry.status}
              </td>
              <td>{entry.brightness}%</td>
              <td>{entry.power}W</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
