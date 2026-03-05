import sys
import os
from pathlib import Path

# --- Symbiote Bootstrap (Directive Alpha: Precision) ---
# This ensures that no matter where you run the script from, 
# it finds the 'symbiote' root and adds it to the Python path.
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# ------------------------------------------------------

try:
    from core.models import SymbioteCore
except ImportError as e:
    print(f"✘ Symbiote Error: Could not resolve core.models. {e}")
    sys.exit(1)

def forge(project_name):
    core = SymbioteCore()
    # Path logic using Pathlib for Windows compatibility
    project_dir = core.root / 'workspace' / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create initial project manifest (Directive Eta: Profit/ROI Tracking)
    manifest = project_dir / 'manifest.json'
    with open(manifest, 'w') as f:
        f.write('{"status": "initialized", "version": "0.1", "burn_rate": 0.0}\n')
    
    core.register_project(project_name)
    print(f"[DIR] Workspace created at: {project_dir}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        forge(sys.argv[1])
    else:
        print("Usage: python shell/forge.py [project_name]")