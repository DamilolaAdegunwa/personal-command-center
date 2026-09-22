# Production Operations Runbook

**System:** Personal Command Center (Personal OS)  
**Tier:** Local Tactical Infrastructure  
**Author:** Operations Engineering Department  
**Last Verified:** 2026-09-22  

---

## 1. System Health Verification

### 1.1 HTTP Health Probe
Verify that the application server process is running and responding:
```bash
curl -f http://127.0.0.1:8000/api/health
```
**Expected Response:** HTTP 200 OK
```json
{"status": "operational", "system": "Personal Command Center (Personal OS)", "version": "1.0.0"}
```

### 1.2 Process Status Verification
Check if the Uvicorn worker process is active:
```bash
pgrep -fl "uvicorn app.main:app"
```

### 1.3 Database Integrity & WAL Mode Verification
Verify that the SQLite database is healthy and actively operating in WAL mode:
```bash
sqlite3 personal_os.db "PRAGMA journal_mode;"
# Expected output: wal

sqlite3 personal_os.db "PRAGMA integrity_check;"
# Expected output: ok
```

---

## 2. Standard Operating Procedures (SOP)

### SOP-01: Routine Database Backup
Execute a live atomic backup without locking read transactions:
```bash
mkdir -p backups
sqlite3 personal_os.db ".backup 'backups/personal_os_$(date +%Y%m%d_%H%M%S).db'"
```

### SOP-02: Graceful Server Restart
```bash
# Locate existing Uvicorn PID
PID=$(pgrep -f "uvicorn app.main:app")

if [ -n "$PID" ]; then
    echo "Terminating PID $PID..."
    kill -15 "$PID"
    sleep 1
fi

# Relaunch via run script
./run.sh &
```

### SOP-03: Manual WAL Checkpoint & Compaction
If `personal_os.db-wal` exceeds 50MB, force a WAL truncation:
```bash
sqlite3 personal_os.db "PRAGMA wal_checkpoint(TRUNCATE);"
```

---

## 3. Incident Diagnostic & Recovery Procedures

### INC-01: "database is locked" (OperationalError)
- **Symptom:** API requests return HTTP 500 with `sqlite3.OperationalError: database is locked`.
- **Root Cause:** A long-running write transaction or hanging Python process is holding an exclusive write lock beyond the 5,000ms `busy_timeout`.
- **Diagnostic Procedure:**
  1. Check for stale processes accessing `personal_os.db`:
     ```bash
     lsof personal_os.db
     ```
  2. If multiple Python processes appear, kill orphaned processes:
     ```bash
     kill -9 <ORPHAN_PID>
     ```
  3. Verify database accessibility:
     ```bash
     sqlite3 personal_os.db "SELECT COUNT(*) FROM tasks;"
     ```

### INC-02: SQLite Database Corruption
- **Symptom:** Server crashes on startup with `DatabaseError: database disk image is malformed`.
- **Root Cause:** Unclean power cut during write flush without fsync, or direct file tampering.
- **Recovery Procedure:**
  1. Immediately quarantine corrupted files:
     ```bash
     mv personal_os.db personal_os.db.corrupt
     mv personal_os.db-wal personal_os.db-wal.corrupt 2>/dev/null || true
     ```
  2. Attempt SQLite recovery dump:
     ```bash
     sqlite3 personal_os.db.corrupt ".recover" | sqlite3 personal_os.db.recovered
     ```
  3. Validate recovered database:
     ```bash
     sqlite3 personal_os.db.recovered "PRAGMA integrity_check;"
     ```
  4. If valid, promote recovered database:
     ```bash
     mv personal_os.db.recovered personal_os.db
     ```
  5. If recovery fails, restore latest daily backup from `backups/`.

### INC-03: Gemini API Quota Exhaustion or Timeout
- **Symptom:** Logs show `google.genai.errors.APIError` or 429 Rate Limit.
- **Operational Reality:** The application is architected with graceful fallback. When Gemini errors out, `AIService._call_gemini_if_available` returns `None`, and the local deterministic heuristic generator produces the briefing immediately.
- **Resolution:**
  - Verify API key quota in Google Cloud Console.
  - No system restart is required.

---

## 4. Escalation & Ownership Matrix

| Area | Primary Contact | Escalation SLA |
|---|---|---|
| Core Architecture & API | System Author (Damilola Adegunwa) | < 2 Hours |
| Database & Persistence | Database Administrator | < 1 Hour |
| Operational Support | DevOps / Runbook Maintainer | < 30 Minutes |
