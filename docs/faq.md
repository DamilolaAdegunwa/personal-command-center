# Frequently Asked Questions (FAQ)

This FAQ provides verified, evidence-based answers to common questions asked by engineers across different disciplines.

---

## 1. Questions from New Developers

### Q: How do I get the application running locally in under 60 seconds?
**A:** Ensure you have Python 3.14+ installed. Run:
```bash
./run.sh
```
The script automatically finds your local virtual environment (or system Python), installs or verifies dependencies, initializes the SQLite database with demonstration data, and boots the server at `http://127.0.0.1:8000`.

### Q: Do I need to install Node.js, npm, or any frontend build tools?
**A:** No. The frontend is built entirely using native browser standards (HTML5, Vanilla CSS with custom properties, and native ES6 JavaScript modules). You simply edit files in `static/` and refresh your browser.

### Q: Where is my data saved, and how do I back it up?
**A:** All data is saved locally in `personal_os.db` in the repository root (or the path set in `COMMAND_CENTER_DB`). To create an atomic backup, run:
```bash
sqlite3 personal_os.db ".backup 'backups/my_backup.db'"
```

---

## 2. Questions from Software Architects

### Q: Why was SQLite selected over a client-server database like PostgreSQL?
**A:** The Personal Command Center is designed for local sovereignty, zero cloud lock-in, and instant zero-daemon portability. In SQLite WAL mode, query latencies are sub-millisecond, eliminating network socket round-trips. A single `.db` file encapsulates the user's entire cognitive footprint.

### Q: How does the system handle concurrent read and write transactions?
**A:** In `app/database.py`, SQLite is explicitly configured with `PRAGMA journal_mode = WAL;` (Write-Ahead Logging) and `PRAGMA busy_timeout = 5000;`. WAL mode allows unlimited concurrent readers without blocking writes. The 5-second busy timeout prevents lock collisions during concurrent operations.

### Q: Why is there no external message broker (Celery, Kafka, Redis)?
**A:** The v1.0.0 architecture operates as a low-overhead, synchronous in-process personal operating system. Eliminating external brokers keeps the deployment footprint to a single lightweight Python process while delivering sub-millisecond response times.

---

## 3. Questions from DevOps & SREs

### Q: What health endpoints exist for automated uptime monitoring?
**A:** `GET /api/health` returns HTTP 200 with `{"status": "operational", "system": "Personal Command Center (Personal OS)", "version": "1.0.0"}`.

### Q: What happens if the Google Gemini API is unreachable or rate-limited?
**A:** The system incorporates a zero-failure fallback. In `app/ai_service.py`, any failure when connecting to `google.genai` is caught, and the system instantly invokes its internal deterministic rule engine. The user receives a high-quality, grounded daily briefing without errors or delay.

### Q: Can I containerize this application with Docker?
**A:** Yes. A complete Dockerfile and Docker Compose specification is provided in [docs/deployment/index.md](deployment/index.md). Be sure to mount a host directory to `/data` to persist `personal_os.db`.

---

## 4. Questions from QA & Test Engineers

### Q: How do automated tests verify AI features without flaky external LLM calls?
**A:** In `tests/test_ai_workflows.py`, tests run in offline mode without requiring a `GEMINI_API_KEY`. The tests verify that the deterministic grounding engine correctly extracts database context, calculates real project counts, and produces the mandatory truth markers (`[FACT]`, `[AI RECOMMENDATION]`).

### Q: How do I run the automated test suite?
**A:** Run:
```bash
PYTHONPATH=. pytest -v tests/
```
All 17 integration and AI workflow tests should pass with zero failures.

---

## 5. Questions from Security Engineers

### Q: Where is `GEMINI_API_KEY` stored, and could it be leaked?
**A:** `GEMINI_API_KEY` is loaded purely into process memory from the environment. It is never persisted in SQLite, never committed to git, and never rendered in API responses or HTML templates.

### Q: Is there any risk of SQL injection?
**A:** No. All database interactions in `app/repository.py` strictly utilize parameterized SQL statements (`?` markers). String formatting (`f"..."` or `%s`) is completely avoided in SQL construction.
