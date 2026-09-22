# Development Workflows

This document outlines everyday development workflows, command references, and testing procedures for the **Personal Command Center**.

---

## 1. Command Quick Reference

The repository provides a `Makefile` containing verified developer shortcuts:

| Target | Command Executed | Purpose |
|---|---|---|
| `make run` | `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload` | Launch development server with hot-reload |
| `make test` | `PYTHONPATH=. pytest -v tests/` | Execute entire automated pytest suite |
| `make seed` | `PYTHONPATH=. python -m app.seed_data` | Populate or verify baseline demonstration data |
| `make clean` | `find . -type d -name "__pycache__" -exec rm -rf {} +` | Purge compiled bytecode and pytest cache |

---

## 2. Testing Workflows

### 2.1 Running the Full Test Suite
```bash
# Run tests with verbose output
PYTHONPATH=. pytest -v tests/
```

### 2.2 Running a Targeted Test File
```bash
# Run only API endpoint tests
PYTHONPATH=. pytest -v tests/test_api.py

# Run only AI grounding and workflow tests
PYTHONPATH=. pytest -v tests/test_ai_workflows.py
```

### 2.3 Running Specific Test Cases
```bash
# Run only the daily briefing test
PYTHONPATH=. pytest -v tests/test_ai_workflows.py -k "test_daily_briefing"
```

---

## 3. Database Management Workflows

### 3.1 Seeding Demonstration Records
If starting with an empty database or fresh environment:
```bash
python3 -m app.seed_data
```

### 3.2 Complete Database Reset
To wipe all state and restore pristine baseline demo records:
```bash
# 1. Stop the running server
# 2. Delete the SQLite database and its WAL files
rm -f personal_os.db personal_os.db-wal personal_os.db-shm

# 3. Start the server (lifespan automatically reinitializes and seeds)
./run.sh
```

### 3.3 Inspecting SQLite via CLI
You can inspect the relational database directly using the standard `sqlite3` CLI:
```bash
sqlite3 personal_os.db

-- Show all tables
.tables

-- Inspect task priority distribution
SELECT priority, status, COUNT(*) FROM tasks GROUP BY priority, status;

-- Inspect project health
SELECT title, health, progress_pct FROM projects;

-- Exit CLI
.quit
```

---

## 4. Frontend Development Workflow

1. **No Bundler / No Node.js Required:**
   - The frontend is served directly from the `static/` directory.
   - Files:
     - `static/index.html`: DOM layout, HUD panels, and modal templates.
     - `static/css/style.css`: Theme variables, grid layout, animations.
     - `static/js/app.js`: Application state and event bindings.
     - `static/js/api.js`: REST fetch helper functions.
     - `static/js/graph.js`: SVG force-directed knowledge graph layout.
2. **Editing & Verifying:**
   - Make your edits to any file in `static/`.
   - Reload your browser (`Cmd+R` / `F5`).
   - Monitor the browser Developer Tools console (`Cmd+Option+I`) for network calls and client logs.
