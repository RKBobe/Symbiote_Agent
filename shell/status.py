import sqlite3
import os
from pathlib import Path

# Force paths
BASE_DIR = Path("D:/symbiote")
DB_PATH = BASE_DIR / "core" / "brain.db"

def show_status():
    # Use standard text instead of emojis to prevent encoding crashes
    print("\n" + "="*40)
    print(" [!] SYMBIOTE SYSTEM STATUS")
    print("="*40)

    if not DB_PATH.exists():
        print(f"Error: Database not found at {DB_PATH}")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. Projects
        print("\n[ ACTIVE PROJECTS ]")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        if cursor.fetchone():
            cursor.execute("SELECT name FROM projects")
            projs = cursor.fetchall()
            if not projs:
                print("  - No active projects.")
            for p in projs:
                print(f"  > {p[0]}")
        else:
            print("  - Projects table not initialized.")

        # 2. Market Pulse
        print("\n[ MARKET PULSE ]")
        cursor.execute("SELECT trend_name, hype_level FROM market_trends ORDER BY id DESC LIMIT 5")
        trends = cursor.fetchall()
        for t in trends:
            print(f"  + {t[0]} (Hype: {t[1]}/10)")

        # 3. Core Health
        print("\n[ CORE HEALTH ]")
        print(f"  - Root: {BASE_DIR}")
        print(f"  - DB:   Connected")

        conn.close()
    except Exception as e:
        print(f"Status Error: {e}")

    print("\n" + "="*40)

if __name__ == "__main__":
    show_status()