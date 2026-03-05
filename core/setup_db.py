import sqlite3
import os
from pathlib import Path

# --- Symbiote Path Logic ---
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / 'core' / 'brain.db'

def initialize():
    print(f"--- 🛠️ Initializing Symbiote Database at {DB_PATH} ---")
    
    # Ensure the 'core' directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # 1. Projects (Directive Eta: Profit/ROI)
            cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                status TEXT DEFAULT 'active',
                stack TEXT,
                estimated_roi REAL DEFAULT 0.0,
                burn_rate REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            # 2. Market Trends (Directive Iota: Market Pulse)
            cursor.execute('''CREATE TABLE IF NOT EXISTS market_trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trend_name TEXT UNIQUE,
                hype_level INTEGER,
                sentiment TEXT,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            # 3. Audit Logs (Directive Zeta: Efficiency)
            cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                waste_detected TEXT,
                optimization_suggestion TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                
            conn.commit()
            print("✔ Database and all tables created successfully.")
            
    except Exception as e:
        print(f"✘ Setup Failed: {e}")

if __name__ == "__main__":
    initialize()