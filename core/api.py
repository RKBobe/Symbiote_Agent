import sys
import os
import subprocess
import sqlite3
from pathlib import Path
from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# --- UTF-8 Enforcement for Windows ---
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# --- Path Configuration ---
# Setting absolute path to ensure DB and Templates are always found
ROOT_DIR = Path("D:/symbiote")
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.models import SymbioteCore

app = FastAPI(title="Symbiote_OS")
templates = Jinja2Templates(directory=str(ROOT_DIR / "core" / "templates"))
core = SymbioteCore()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    projects = []
    trends = []
    
    try:
        # Connect using the absolute path from our core model
        with sqlite3.connect(core.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Fetch Projects (Fixed: Removed 'path' column which caused crashes)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
            if cursor.fetchone():
                cursor.execute("SELECT name FROM projects ORDER BY updated_at DESC")
                projects = cursor.fetchall()
            
            # 2. Fetch Trends
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='market_trends'")
            if cursor.fetchone():
                cursor.execute("SELECT trend_name, hype_level FROM market_trends ORDER BY id DESC LIMIT 10")
                trends = cursor.fetchall()
            
            print(f"DEBUG: Found {len(projects)} projects and {len(trends)} trends in {core.db_path}")

    except Exception as e:
        print(f"CRITICAL UI ERROR: {e}")
        # Keep lists empty so the page still loads but shows the error in console
        
    return templates.TemplateResponse("index.html", {
        "request": request,
        "projects": projects,
        "trends": trends
    })

@app.post("/terminal")
async def terminal_input(command: str = Body(..., embed=True)):
    try:
        # Run commands relative to the D:/symbiote root
        # Redirecting stderr to stdout so we see errors in the browser
        result = subprocess.check_output(
            command, 
            shell=True, 
            stderr=subprocess.STDOUT, 
            text=True,
            cwd=str(ROOT_DIR),
            encoding='utf-8' # Force UTF-8 for command output
        )
        return {"output": result}
    except subprocess.CalledProcessError as e:
        return {"output": e.output if e.output else "Command failed with no output."}
    except Exception as e:
        return {"output": f"System Error: {str(e)}"}