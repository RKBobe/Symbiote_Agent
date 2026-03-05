import sys
import sqlite3
import os
from pathlib import Path

def add_pulse(trend, hype, notes):
    # Ensure we find the DB even if the env var is finicky
    root = Path(os.getenv('SYMBIOTE_PATH', 'D:/symbiote'))
    db_path = root / "core" / "brain.db"
    
    print(f"[*] Attempting to connect to: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO market_trends (trend_name, hype_level, notes) VALUES (?, ?, ?)",
            (trend, hype, notes)
        )
        conn.commit()
        conn.close()
        print(f"[✔] SUCCESS: Captured '{trend}' at Hype {hype}/10.")
    except Exception as e:
        print(f"[✘] ERROR: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python pulse.py <trend> <hype> <notes>")
    else:
        add_pulse(sys.argv[1], int(sys.argv[2]), sys.argv[3])