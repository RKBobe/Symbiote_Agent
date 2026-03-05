# Symbiote_Agent OS (v1.0)
> **Lead Developer:** RKBobe  
> **Status:** Alpha - Stable Infrastructure

Symbiote is a localized, browser-based Agentic OS designed for market intelligence, project automation, and defense-sector trend tracking.

---

## 🛠 Current Architecture
- **Core Brain:** SQLite-backed intelligence storage (`core/brain.db`).
- **REST Terminal:** Integrated FastAPI web shell for executing PowerShell/Python commands.
- **Project Forge:** Automated workspace generator with database synchronization.
- **Intelligence Scrapers:** Keyword-based market pulse scanners.

## 🚀 Quick Start
1. **Activate Environment:** `.\venv\Scripts\activate`
2. **Launch OS:** `python -m uvicorn core.api:app --reload`
3. **Access Dashboard:** `http://localhost:8000`

---

## 📅 TODO: Phase 2 (Tomorrow's Sprint)

### 🔴 High Priority: Intelligence Depth
- [ ] **NewsAPI Integration:** Replace the basic `scan.py` logic with real-time API calls to fetch global defense news.
- [ ] **Sentiment Analysis:** Add a "Vibe Check" to trends using a lightweight NLP library (or LLM) to rank "Hype" automatically.

### 🟡 Medium Priority: System UX
- [ ] **Forge Templates:** Update `forge.py` to auto-generate a `README.md` and `requirements.txt` inside every new project folder.
- [ ] **Live Logs:** Add a scrolling log window to the `index.html` to see the Symbiote's background "thoughts" in real-time.

### 🟢 Low Priority: Housekeeping
- [ ] **Database UI:** Add a "Clear Brain" button to the terminal to reset trends.
- [ ] **Style Overhaul:** Refine the CSS for a true "Dark Mode" terminal aesthetic.

---

## 🔒 Security Note
The `.gitignore` is configured to prevent the upload of `brain.db` and `venv/`. Local project workspaces are kept private to ensure data sovereignty.
