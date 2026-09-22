# Troubleshooting Matrix & Diagnostic Guide

This guide provides an evidence-based troubleshooting matrix for identifying and resolving issues across the **Personal Command Center** platform.

---

## 1. Quick Troubleshooting Matrix

| Symptom | Possible Cause | Diagnostic Steps | Resolution |
|---|---|---|---|
| `[Errno 48] Address already in use` | Another instance or background process is already bound to port 8000 | Run `lsof -i :8000` to find the process holding the port | Terminate the existing process via `kill -15 <PID>` or launch on an alternative port: `PORT=8080 ./run.sh` |
| `sqlite3.OperationalError: database is locked` | Stale process holding write lock, or write transaction exceeded 5,000ms timeout | Run `lsof personal_os.db` | Kill orphaned processes holding open SQLite handles: `kill -9 <PID>` |
| `ModuleNotFoundError: No module named 'fastapi'` | Virtual environment not activated or dependencies uninstalled | Run `which python3` and check if inside `.venv` | Activate environment (`source .venv/bin/activate`) and run `pip install -r requirements.txt` |
| `PermissionError: [Errno 13] Permission denied: 'personal_os.db'` | Insufficient filesystem write permissions on current directory | Run `ls -ld . personal_os.db` | Fix directory permissions: `chmod u+rw . personal_os.db*` |
| `HTTP 422 Unprocessable Entity` on API requests | Invalid JSON schema payload (e.g. invalid enum value, out-of-bounds percentage) | Inspect response body JSON `detail` array | Verify request payload against [docs/api/schemas.md](../api/schemas.md) |
| `HTTP 404 Not Found` for project, idea, or task | Record was deleted or invalid UUID supplied in path | Query SQLite directly: `sqlite3 personal_os.db "SELECT * FROM projects WHERE id='<ID>';"` | Verify the entity ID exists in the database |
| Omni-Search (`Cmd+K`) yields 0 results | Database is unseeded, or filter tokens do not match text | Check record count: `curl http://127.0.0.1:8000/api/today` | Seed sample data via `POST /api/seed` or `make seed` |
| Knowledge Graph renders empty canvas | No entities exist, or SVG dimensions collapsed in DOM | Check browser console (`Cmd+Opt+I`) for `getGraph` payload | Confirm records exist; verify browser window is visible and SVG container is styled |
| AI Daily Briefing shows generic deterministic text | `GEMINI_API_KEY` is not set or Google API quota exceeded | Check server logs for `google.genai` errors | Normal fallback behavior; to enable Gemini, set `export GEMINI_API_KEY="AIzaSy..."` |
| Task `completed_at` remains `null` | Task was updated without setting `status = 'completed'` | Inspect database row: `SELECT status, completed_at FROM tasks WHERE id='...';` | Transition task to completed via `PUT /api/tasks/{id}` with `{"status": "completed"}` |

---

## 2. In-Depth Diagnostic Workflows

### 2.1 Resolving Port Binding Collisions
```bash
# 1. Identify which process is listening on port 8000
lsof -i :8000

# Example output:
# COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
# Python  34521 dammy    6u  IPv4 ...      0t0  TCP localhost:irdmi (LISTEN)

# 2. Terminate the stale PID
kill -15 34521

# 3. Confirm port is free
lsof -i :8000
```

### 2.2 Diagnosing Database Lock Contention
```bash
# 1. Inspect open file handles for personal_os.db
lsof personal_os.db

# 2. Verify WAL mode and foreign key state
sqlite3 personal_os.db "PRAGMA journal_mode; PRAGMA foreign_keys;"

# 3. Test read responsiveness
sqlite3 personal_os.db "SELECT COUNT(*) FROM tasks;"
```

### 2.3 Inspecting Browser Network Failures
1. In Chrome / Brave / Edge, open Developer Tools: `Cmd + Option + I` (macOS) or `Ctrl + Shift + I` (Linux/Windows).
2. Select the **Network** tab.
3. Trigger the failing action in the HUD.
4. Click on the red HTTP request. Inspect the **Payload** and **Response** tabs to see the precise Pydantic error details.
