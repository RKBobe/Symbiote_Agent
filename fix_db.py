import sqlite3
from pathlib import Path

db_path = Path("D:/symbiote/core/brain.db")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO market_trends (trend_name, hype_level, notes) VALUES (?, ?, ?)", 
                   ('System_Check', 10, 'Manual bridge successful'))
    conn.commit()
    conn.close()
    print("--- DB Injection Successful ---")
except Exception as e:
    print(f"--- Injection Failed: {e} ---")
