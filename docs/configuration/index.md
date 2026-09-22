# Configuration Reference

This document provides a systematic catalog of all configuration parameters, environment variables, and runtime defaults utilized by the **Personal Command Center**.

---

## 1. Environment Variables Catalog

| Variable Name | Purpose | Expected Type | Default Value | Required? | Consumed In | Sensitivity |
|---|---|---|---|---|---|---|
| `COMMAND_CENTER_DB` | Filesystem path to primary SQLite database file | String (Path) | `<repo_root>/personal_os.db` | No | `app/database.py` | Low |
| `GEMINI_API_KEY` | Google Gemini API secret key for AI intelligence studio | String (API Key) | `None` (Unset) | No | `app/ai_service.py` | **High (Secret)** |
| `PORT` | TCP listening port for Uvicorn web server | Integer / String | `8000` | No | `run.sh`, `Makefile` | Low |
| `HOST` | IP address interface for Uvicorn binding | String (IP) | `127.0.0.1` | No | `run.sh` | Medium |

---

## 2. In-Depth Setting Descriptions

### 2.1 `COMMAND_CENTER_DB`
- **Description:** Directs the database connection manager to a custom file location.
- **Consumption:** Evaluated once at module import in `app/database.py`:
  ```python
  DB_PATH = os.getenv("COMMAND_CENTER_DB", str(Path(__file__).parent.parent / "personal_os.db"))
  ```
- **Operational Considerations:**
  - The executing process must have read and write permissions to both the directory and the target database file.
  - SQLite creates auxiliary `-wal` and `-shm` files in the exact same directory as the target database.

### 2.2 `GEMINI_API_KEY`
- **Description:** Authenticates outbound HTTPS requests to Google's Generative AI service (`generativelanguage.googleapis.com`) using `gemini-2.5-flash`.
- **Consumption:** Evaluated dynamically in `app/ai_service.py`:
  ```python
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  ```
- **Fallback Behavior:**
  - If omitted or empty, `_call_gemini_if_available()` returns `None`.
  - The application automatically switches to its local deterministic rule engine.
  - Zero crashes, zero network timeouts, zero degradation of core workflows.
- **Security Warning:**
  > [!CAUTION]
  > Never commit `GEMINI_API_KEY` into git repositories, shell scripts, or documentation. Always inject it via shell environment variables or local `.env` files that are strictly included in `.gitignore`.

### 2.3 `HOST` and `PORT`
- **Description:** Configures network socket binding for Uvicorn.
- **Security Guidance:**
  - Defaults to `127.0.0.1` (loopback only).
  - Do NOT bind to `0.0.0.0` unless running within a secure, isolated container or behind an authenticated reverse proxy, as the application currently enforces no client authentication.

---

## 3. Database Engine Pragmas

The database configuration in `app/database.py` applies three critical SQLite runtime pragmas upon connection acquisition:

```python
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn
```

1. **`PRAGMA journal_mode = WAL;`**
   - Enables Write-Ahead Logging. Readers do not block writers, and writers do not block readers. Substantially increases concurrency.
2. **`PRAGMA foreign_keys = ON;`**
   - Enforces referential integrity. Ensures `ON DELETE SET NULL` cascades correctly when projects or ideas are deleted.
3. **`PRAGMA busy_timeout = 5000;`**
   - Instructs SQLite to sleep and retry for up to 5,000 milliseconds if a database table is locked by another write transaction before raising an `OperationalError`.
