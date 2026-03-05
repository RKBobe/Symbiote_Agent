import sqlite3
import os
from pathlib import Path
from datetime import datetime

class SymbioteCore:
    def __init__(self):
        # Pathlib automatically handles \ vs / for Windows/Linux
        self.root = Path(os.getenv('SYMBIOTE_PATH', Path(__file__).parent.parent))
        self.db_path = self.root / 'core' / 'brain.db'
        self._ensure_dirs()
        self._init_db()

    def _ensure_dirs(self):
        """Ensures the core and workspace directories exist."""
        (self.root / 'core').mkdir(parents=True, exist_ok=True)
        (self.root / 'workspace').mkdir(parents=True, exist_ok=True)

    def _init_db(self):
        """Initializes the SQLite schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Projects Table
                cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    status TEXT DEFAULT 'active',
                    stack TEXT,
                    estimated_roi REAL DEFAULT 0.0,
                    burn_rate REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"✘ Database Error: {e}")
            
    def register_project(self, name, stack='general', roi=0.0):
        from datetime import datetime
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''INSERT INTO projects (name, stack, estimated_roi, updated_at) 
                          VALUES (?, ?, ?, ?)
                          ON CONFLICT(name) DO UPDATE SET 
                          updated_at=excluded.updated_at''', 
                          (name, stack, roi, datetime.now()))
        # Removed the emoji to prevent Windows encoding crashes
        print(f"[SUCCESS] Symbiote DB: '{name}' is online.")
        
if __name__ == "__main__":
    SymbioteCore()
    print("🚀 Symbiote Core Engine Online.")