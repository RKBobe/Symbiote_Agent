import time
import os
from watchdog.observers.polling import PollingObserver as Observer # Swapped to Polling
from watchdog.events import FileSystemEventHandler
from core.intel_engine import IntelEngine

INTEL_DIR = r"D:\symbiote\core\intelligence"
if not os.path.exists(INTEL_DIR):
    os.makedirs(INTEL_DIR)
    
intel = IntelEngine()
WATCH_PATH = os.path.abspath("intelligence")

class IngestHandler(FileSystemEventHandler):
    def process(self, event):
        # Ignore directories and non-txt files
        if event.is_directory or not event.src_path.endswith(".txt"):
            return
            
        print(f">> ACTIVITY DETECTED: {os.path.basename(event.src_path)}")
        time.sleep(1) # Wait for file lock to release
        report_id = os.path.basename(event.src_path).replace(".txt", "")
        result = intel.ingest_report(report_id, event.src_path)
        print(f">> {result}")

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

if __name__ == "__main__":
    if not os.path.exists(WATCH_PATH):
        os.makedirs(WATCH_PATH)
        
    event_handler = IngestHandler()
    observer = Observer() # Now using PollingObserver
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    print(f">> SYMBIOTE WATCHER ACTIVE (POLLING MODE): {WATCH_PATH}")
    
    # --- PRE-SCAN: Ingest existing files on startup ---
    print(">> RUNNING INITIAL SCAN...")
    for f in os.listdir(INTEL_DIR):
        if f.endswith(".txt") or f.endswith(".pdf"):
            full_path = os.path.join(INTEL_DIR, f)
    for f in os.listdir(WATCH_PATH):
        if f.endswith(".txt"):
            full_path = os.path.join(WATCH_PATH, f)
            intel.ingest_report(f.replace(".txt", ""), full_path)
    print(">> INITIAL SCAN COMPLETE.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()