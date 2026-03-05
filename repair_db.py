import sqlite3
from pathlib import Path

db_path = Path("D:/symbiote/core/brain.db")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Add the missing column
    try:
        cursor.execute("ALTER TABLE market_trends ADD COLUMN notes TEXT")
        print("[*] Column 'notes' added successfully.")
    except sqlite3.OperationalError:
        print("[!] Column 'notes' might already exist or table is locked.")

    # 2. Try the injection again
    cursor.execute("INSERT INTO market_trends (trend_name, hype_level, notes) VALUES (?, ?, ?)", 
                   ('System_Check', 10, 'Schema repair successful'))
    
    conn.commit()
    conn.close()
    print("[✔] DB Corrected and Injection Successful.")
except Exception as e:
    print(f"[✘] Migration Failed: {e}")
