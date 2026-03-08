import sqlite3
from pathlib import Path

# Target project keywords
KEYWORDS = ["Anthropic", "Pentagon", "Defense", "Military", "AI Safety", "Dario"]

BASE_DIR = Path("D:/symbiote")
DB_PATH = BASE_DIR / "core" / "brain.db"
REPORT_PATH = Path(__file__).parent / "intelligence_report.txt"

def run_project_scan():
    print(f"--- Running Intelligence Scan for: Anthropic Pentagon Tracker ---")
    
    if not DB_PATH.exists():
        print("Error: Core Brain not found.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Search for any market trends matching our keywords
        query = "SELECT trend_name, hype_level FROM market_trends WHERE " + " OR ".join(["trend_name LIKE ?"] * len(KEYWORDS))
        params = [f"%{k}%" for k in KEYWORDS]
        
        cursor.execute(query, params)
        findings = cursor.fetchall()

        # Generate Report
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write("=== PROJECT INTELLIGENCE REPORT ===\n")
            f.write(f"Target: Anthropic/Pentagon Connection\n\n")
            
            if findings:
                f.write(f"Found {len(findings)} relevant data points:\n\n")
                for trend, hype in findings:
                    f.write(f"  [!] {trend} (Hype: {hype}/10)\n")
                print(f"[MATCH] Found {len(findings)} matches. Report updated.")
            else:
                f.write("No direct matches found in current Brain cycle.\n")
                print("[i] No new matches found.")

        conn.close()
    except Exception as e:
        print(f"Agent Error: {e}")

if __name__ == "__main__":
    run_project_scan()