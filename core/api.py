from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os

# Import our Intelligence Engine
from core.intel_engine import IntelEngine

app = FastAPI(title="Symbiote OS Intelligence Core")

# --- MOUNT STATIC ASSETS ---
# This allows the browser to find /static/style.css and /static/app.js
app.mount("/static", StaticFiles(directory="core/static"), name="static")

# --- SETUP TEMPLATES ---
templates = Jinja2Templates(directory="core/templates")

# Initialize the Intelligence Engine
# Note: If this hangs, ensure your Gemini API Key is set in intel_engine.py
try:
    intel = IntelEngine()
except Exception as e:
    print(f"CRITICAL: IntelEngine failed to load: {e}")
    intel = None

# Mock data for the UI (Replace with your DB logic later)
projects = [["anthropic_pentagon_tracker", "Active"], ["market_pulse_v2", "Idle"]]
trends = [["AI_REGULATION", 85], ["QUANTUM_COMPUTING", 42], ["PENTAGON_CONTRACTS", 91]]

class CommandRequest(BaseModel):
    command: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "projects": projects, 
        "trends": trends
    })

@app.get("/status")
async def get_status():
    """Returns the status of the AI Engine for the UI LED."""
    return {"status": "online" if intel is not None else "offline"}

@app.post("/query")
async def query_intel(payload: dict = Body(...)):
    """
    RAG Pipeline: 
    1. Search Vector DB 
    2. Synthesize with Gemini
    """
    question = payload.get("question")
    if not intel:
        return {"answer": "SYSTEM ERROR: Intelligence Engine is offline."}
    
    try:
        # Step 1: Retrieve context from ChromaDB
        snippets = intel.query(question)
        
        # Step 2: Pass snippets + question to Gemini for a smart answer
        answer = intel.synthesize(question, snippets)
        
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"SYNTHESIS ERROR: {str(e)}"}

@app.post("/terminal")
async def run_terminal(req: CommandRequest):
    """Simple terminal command handler."""
    cmd = req.command.lower()
    
    if cmd == "help":
        return {"output": "Available: status, clear_cache, ingest_all, whoami"}
    elif cmd == "whoami":
        return {"output": "User: RKBobe | Role: System Administrator"}
    elif cmd == "status":
        status = "ONLINE" if intel else "OFFLINE"
        return {"output": f"AI_CORE: {status} | DATABASE: CONNECTED"}
    else:
        return {"output": f"Command '{cmd}' not recognized by Symbiote Kernel."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)