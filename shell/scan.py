import sqlite3
import urllib.request
import xml.etree.ElementTree as ET
import os
from pathlib import Path

# Absolute pathing to ensure it works regardless of where you call it from
BASE_DIR = Path("D:/symbiote")
DB_PATH = BASE_DIR / "core" / "brain.db"

def fetch_trends():
    # RSS Feed for Hacker News - filtered for items with at least 10 points
    url = "https://hnrss.org/newest?points=10"
    print(f"[*] Connecting to Nerve Center (RSS)...")
    
    try:
        # 1. Fetch Data
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(request) as response:
            tree = ET.parse(response)
            root = tree.getroot()
        
        # 2. Connect to Brain
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        found = 0
        # 3. Process the top 10 items
        for item in root.findall("./channel/item")[:10]:
            title = item.find("title").text
            link = item.find("link").text
            
            # Using INSERT OR IGNORE to prevent duplicate headlines
            cursor.execute("""
                INSERT OR IGNORE INTO market_trends (trend_name, hype_level, notes) 
                VALUES (?, ?, ?)
            """, (title[:60], 7, f"Source: {link}"))
            
            if cursor.rowcount > 0:
                found += 1
        
        conn.commit()
        conn.close()
        print(f"[✔] Scan complete. Injected {found} new trends into the Brain.")
        
    except Exception as e:
        print(f"[✘] Scan failed: {str(e)}")

if __name__ == "__main__":
    # Ensure the core directory exists before trying to hit the DB
    os.makedirs(DB_PATH.parent, exist_ok=True)
    fetch_trends()