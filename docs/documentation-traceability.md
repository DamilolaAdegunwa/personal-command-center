# Documentation Traceability Matrix

This document maps core architectural claims, API endpoints, schema definitions, and business logic documented across the **Personal Command Center** directly to verified source code locations.

---

## 1. Traceability Standard

Each technical assertion is categorized by an evidence-based confidence level:
- **Verified:** Directly corroborated by executed source code, schema DDL, or unit test assertions.
- **Strongly Inferred:** Extracted from runtime configurations, default environment behavior, or build manifests.
- **Inferred:** Deduced from structural dependencies or architectural patterns.
- **Roadmap / Planned:** Documented in roadmap specifications; verified as not yet implemented in code.

---

## 2. Evidence Traceability Matrix

| Documentation Claim | Primary Repository Source | Source Lines | Confidence Level | Verification Notes |
|---|---|---|---|---|
| **FastAPI REST Application** | `app/main.py` | L39-44 | **Verified** | `app = FastAPI(title="Personal Command Center", ...)` |
| **CORS Wildcard Policy** | `app/main.py` | L47-53 | **Verified** | `allow_origins=["*"]` configured |
| **Static File Mounting** | `app/main.py` | L56-57 | **Verified** | `app.mount("/static", ...)` mounts local static directory |
| **All 24 REST Endpoints** | `app/main.py` | L59-415 | **Verified** | Route decorators `@app.get`, `@app.post`, etc. |
| **SQLite WAL Journal Mode** | `app/database.py` | L12 | **Verified** | `PRAGMA journal_mode = WAL;` executed on connect |
| **Foreign Key Enforcement** | `app/database.py` | L13 | **Verified** | `PRAGMA foreign_keys = ON;` executed on connect |
| **Busy Timeout (5000ms)** | `app/database.py` | L14 | **Verified** | `PRAGMA busy_timeout = 5000;` executed on connect |
| **9 Relational Tables** | `app/database.py` | L21-200 | **Verified** | Schema DDL executes `CREATE TABLE IF NOT EXISTS` |
| **15 Performance Indexes** | `app/database.py` | L40-200 | **Verified** | Explicit `CREATE INDEX IF NOT EXISTS` statements |
| **UUIDv4 Primary Keys** | `app/repository.py` | L90, L209, etc. | **Verified** | Primary keys generated using `str(uuid.uuid4())` |
| **Task Completion Stamping**| `app/repository.py` | L92, L120-123 | **Verified** | `completed_at` set when status becomes `completed` |
| **7-Stage Idea Lifecycle** | `app/models.py`, `app/main.py` | L52-60, L154 | **Verified** | Enforced by `IdeaStatus` enum and transition route |
| **4-Bracket Grounding** | `app/ai_service.py` | L60-62, L87-128 | **Verified** | `[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, `[AI RECOMMENDATION]` |
| **Gemini 2.5 Flash Model** | `app/ai_service.py` | L19 | **Verified** | `model="gemini-2.5-flash"` invoked via `google-genai` |
| **Deterministic Fallback** | `app/ai_service.py` | L84-129 | **Verified** | Local rule generator executes if API key unset |
| **P0 Task Priority Rank** | `app/repository.py` | L41 | **Verified** | SQL `ORDER BY CASE priority WHEN 'p0_critical' THEN 0 ...` |
| **72-Hour Deadline Horizon**| `app/ai_service.py` | L44-55 | **Verified** | Incomplete tasks with deadline diff <= 3.0 days |
| **14-Day Stagnation Rule** | `app/metrics_service.py` | L10, L22-29 | **Verified** | Active projects older than 14d flagged as stalled |
| **Implicit Graph Edges** | `app/graph_service.py` | L41-51, L66-87 | **Verified** | FKs resolve to `spawns`, `validates`, and `informs` |
| **Search Scoring Weights** | `app/search_service.py` | L18-29 | **Verified** | +5.0 title, +1.5 content, +1.0 project boost |
| **Default Host & Port** | `run.sh`, `Makefile` | L1-2, L16-17 | **Strongly Inferred** | Defaults to `127.0.0.1` and port `8000` |
| **Absence of Message Broker**| Full Codebase Scan | N/A | **Verified Absent** | Zero Kafka, Celery, or Redis imports in repository |
| **MCP Server Tool Exposure**| `docs/ROADMAP.md` | L15 | **Roadmap** | Planned in Phase 2; not implemented in code |
| **Git Commit Auto-Watcher** | `docs/ROADMAP.md` | L16 | **Roadmap** | Planned in Phase 2; not implemented in code |
