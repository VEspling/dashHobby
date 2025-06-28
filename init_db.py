import sqlite3

conn = sqlite3.connect("eink_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bms_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    data TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mppt_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    data TEXT
)
""")

conn.commit()
conn.close()
print("✅ Databas skapad: eink_data.db")
# This script initializes the SQLite database for storing BMS and MPPT data.
# It creates two tables: bms_data and mppt_data, each with an id, timestamp, and data field.