# System Architecture Specification

This document defines the high-level system architecture, operational boundaries, and structural tiers of the **Personal Command Center**.

---

## 1. System Topology & Tiers

The Personal Command Center is architecturally structured as a decoupled, local-first client-server application composed of three distinct execution layers and an optional external intelligence integration:

```mermaid
flowchart TB
    subgraph ClientLayer ["1. Client Interface Tier"]
        Browser["Modern Browser (Chromium / WebKit / Gecko)"]
        UI["Tactical HUD (HTML5 / Vanilla CSS / ES6)"]
        SVG["Interactive Knowledge Graph (SVG Native)"]
        Browser --> UI
        Browser --> SVG
    end

    subgraph Boundary ["Localhost Boundary (127.0.0.1:8000)"]
        subgraph ServerLayer ["2. Application Server Tier (FastAPI)"]
            ASGI["Uvicorn ASGI Web Server"]
            FastAPIApp["FastAPI Router & Middleware"]
            StaticMount["Static File Mount (/static)"]
            
            subgraph Services ["Application Services"]
                Repo["Repository Layer"]
                GraphEngine["Graph Resolution Engine"]
                SearchEngine["Omni-Search Token Engine"]
                MetricsEngine["Situational Metrics Engine"]
                AIEngine["Grounded AI Studio Engine"]
            end
        end

        subgraph DataLayer ["3. Local Persistence Tier (SQLite WAL)"]
            DBConnection["Connection Pool (busy_timeout=5000ms)"]
            SQLiteFile[("personal_os.db")]
            WALFile["personal_os.db-wal"]
            SHMFile["personal_os.db-shm"]
        end
    end

    subgraph ExternalServices ["4. External Cloud Tier (Optional)"]
        GeminiAPI["Google Gemini LLM Endpoint (gemini-2.5-flash)"]
    end

    UI -->|HTTP GET / POST / PUT / DELETE| ASGI
    ASGI --> FastAPIApp
    FastAPIApp --> StaticMount
    FastAPIApp --> Services
    
    Repo --> DBConnection
    DBConnection --> SQLiteFile
    DBConnection --> WALFile
    DBConnection --> SHMFile
    
    AIEngine -.->|Outbound HTTPS (443) if GEMINI_API_KEY set| GeminiAPI
```

---

## 2. Tier Specifications

### 2.1 Tier 1: Client Interface Tier
- **Technology Stack:** Pure HTML5, Semantic CSS3 (CSS Variables for dark HUD styling), Vanilla ES6 Modules.
- **Delivery Mechanism:** Static files served directly by FastAPI via `app.mount("/static", StaticFiles(directory=...), name="static")`.
- **Root Entry Point:** `@app.get("/")` serves `static/index.html`.
- **State Management:** Local client-side reactive state held in `static/js/app.js`, synchronized via asynchronous REST fetches (`static/js/api.js`).
- **Graph Visualization:** Native SVG DOM manipulation in `static/js/graph.js` with force-simulation coordinates, dynamic edge drawing, and interactive pan/zoom.

### 2.2 Tier 2: Application Server Tier
- **Runtime:** Python 3.14+ executing on macOS / Linux / Windows.
- **Web Framework:** FastAPI 0.115+ running on Uvicorn 0.30+.
- **Lifecycle Management:** Managed via `@asynccontextmanager async def lifespan(app: FastAPI)`:
  - Invokes `app.database.init_db()` to ensure schema existence and create required indexes.
  - Invokes `app.seed_data.seed_database()` to populate demonstration domain records if the database is unseeded.
- **Serialization & Validation:** Pydantic v2 schemas strictly validate every incoming and outgoing JSON structure.

### 2.3 Tier 3: Local Persistence Tier
- **Database Engine:** Embedded SQLite 3.50+.
- **Concurrency & Journaling:**
  - `PRAGMA journal_mode = WAL;` (Write-Ahead Logging permits concurrent readers without blocking writes).
  - `PRAGMA foreign_keys = ON;` (Guarantees relational integrity across foreign keys).
  - `PRAGMA busy_timeout = 5000;` (Waits up to 5 seconds during lock contention before throwing an error).
- **Physical Footprint:** Three files on the host filesystem:
  - `personal_os.db`: Primary database file containing schema and persistent B-trees.
  - `personal_os.db-wal`: Write-ahead log recording uncommitted/pending transactions.
  - `personal_os.db-shm`: Shared-memory index supporting concurrent reader coordination.

### 2.4 Tier 4: Optional External Intelligence Tier
- **Target Service:** Google Gemini Generative AI Platform.
- **Client Library:** `google-genai` Python SDK (`from google import genai`).
- **Model:** `gemini-2.5-flash`.
- **Activation Gate:** Activated exclusively if the `GEMINI_API_KEY` environment variable is defined.
- **Fail-Safe Mechanism:** When the API key is omitted, network calls are never attempted. The system falls back deterministically to local heuristic algorithms with 0ms external latency.

---

## 3. System Boundaries & Network Policy

| Boundary | Inbound Interface | Outbound Interface | Network Protocol | Security Context |
|---|---|---|---|---|
| **Client ➔ Server** | `127.0.0.1:8000` | Localhost loopback | HTTP/1.1 (JSON) | Unauthenticated loopback interface |
| **Server ➔ SQLite** | In-process C API | Local disk I/O | POSIX syscalls | OS file permissions |
| **Server ➔ Gemini** | N/A | `generativelanguage.googleapis.com` | HTTPS (TLS 1.3) / Port 443 | Bearer Token (`GEMINI_API_KEY`) |

---

## 4. Architectural Assumptions & Verified Constraints

1. **Local Single-User Execution:**
   - *Verified Behavior:* The application contains no user tables, authentication middleware, or tenant isolation. It is engineered specifically as a personal operating system for a single individual.
2. **Synchronous Request Model:**
   - *Verified Behavior:* Endpoints in `app/main.py` are declared as standard synchronous functions (`def list_projects()`, `def get_daily_briefing()`) executed by FastAPI within its thread pool.
3. **Ephemeral State Absence:**
   - *Verified Behavior:* The application maintains no state in memory between requests other than the database connection; restarting the server incurs zero data loss.
