# Local Setup & Bootstrapping Guide

This guide walks through configuring your local development environment to run and modify the **Personal Command Center**.

---

## 1. Prerequisites

Before setting up the repository, ensure your system meets the following requirements:

- **Operating System:** macOS (Sonoma / Sequoia recommended), Linux (Ubuntu 22.04+ / Debian 12+), or Windows (via WSL2).
- **Python:** Version `3.14+` installed (or `3.12+` compatible).
- **Git:** Version `2.30+`.
- **Web Browser:** Any modern evergreen browser (Chrome, Brave, Edge, Firefox, Safari).

---

## 2. Step-by-Step Installation

### Step 2.1: Clone the Repository
```bash
git clone https://github.com/DamilolaAdegunwa/personal-command-center.git
cd personal-command-center
```

### Step 2.2: Create and Activate Virtual Environment
```bash
# Create isolated Python virtual environment
python3 -m venv .venv

# Activate on macOS / Linux
source .venv/bin/activate

# Or activate on Windows PowerShell
# .venv\Scripts\Activate.ps1
```

### Step 2.3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Environment Configuration

The application is fully functional out of the box with zero required environment variables. However, optional variables can be set:

```bash
# Optional: Set custom path to SQLite database (defaults to ./personal_os.db)
export COMMAND_CENTER_DB="/path/to/custom_personal_os.db"

# Optional: Enable live Gemini 2.5 Flash intelligence workflows
export GEMINI_API_KEY="AIzaSy..."

# Optional: Override listening host and port (defaults to 127.0.0.1:8000)
export PORT="8000"
export HOST="127.0.0.1"
```

> [!TIP]
> If `GEMINI_API_KEY` is not provided, the application automatically uses its built-in deterministic heuristic engine. All features (Daily Briefing, Project Diagnostics, Idea Stress-Testing, Decision Audits) work immediately without external network access.

---

## 4. Bootstrapping & Launch

Launch the server using any of the following established methods:

### Method A: Using the Convenience Shell Script
```bash
chmod +x run.sh
./run.sh
```

### Method B: Using Make
```bash
make run
```

### Method C: Direct Uvicorn Execution
```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 5. Verification

### Automated Health Verification
In a separate terminal, test the running server:
```bash
curl -s http://127.0.0.1:8000/api/health | jq .
```
Expected output:
```json
{
  "status": "operational",
  "system": "Personal Command Center (Personal OS)",
  "version": "1.0.0"
}
```

### Visual Verification
Open your browser to:
- **Cockpit HUD:** `http://127.0.0.1:8000`
- **Interactive OpenAPI Docs:** `http://127.0.0.1:8000/docs`
- **ReDoc Specification:** `http://127.0.0.1:8000/redoc`
