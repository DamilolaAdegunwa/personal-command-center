# Architecture Specification: Personal Command Center

## 1. High-Level Architecture Overview

The Personal Command Center is architected as a **local-first, low-latency, intelligence-amplified personal operating system**. It marries a high-speed Python/FastAPI backend with a persistent SQLite transactional store and a responsive, high-density Single-Page Interface designed for rapid situational assessment.

```
+-----------------------------------------------------------------------------------+
|                                CLIENT FRONTEND                                    |
|  +------------------+  +-------------------+  +--------------------------------+  |
|  | Tactical HUD View|  | Interactive SVG   |  | Universal Omni-Search (Cmd+K)  |  |
|  | (12 Live Panels) |  | Knowledge Graph   |  | Faceted Filtering Engine       |  |
|  +------------------+  +-------------------+  +--------------------------------+  |
|          |                       |                           |                    |
|          +-----------------------+---------------------------+                    |
|                                  | REST / JSON APIs                               |
+----------------------------------|------------------------------------------------+
                                   v
+-----------------------------------------------------------------------------------+
|                             FASTAPI SERVER BACKEND                                |
|  +-------------------+  +---------------------+  +-----------------------------+  |
|  | Domain Routers    |  | Universal Search    |  | Knowledge Graph Service     |  |
|  | (/api/today, ...) |  | Engine (FTS/Token)  |  | (Node/Edge Resolution)      |  |
|  +-------------------+  +---------------------+  +-----------------------------+  |
|  +--------------------------------------------+  +-----------------------------+  |
|  | Grounded AI Intelligence Studio            |  | Situational Metrics Engine  |  |
|  | (Daily Briefing, Weekly, Project/Idea/Dec) |  | (Velocity, Health, Stalled) |  |
|  +--------------------------------------------+  +-----------------------------+  |
|                                  |                                                |
+----------------------------------|------------------------------------------------+
                                   v
+-----------------------------------------------------------------------------------+
|                              DATA & STORAGE LAYER                                 |
|  +-----------------------------------------------------------------------------+  |
|  | SQLite Relational Engine (WAL Mode, Foreign Key Enforcement, JSON1)         |  |
|  | Schema: tasks, projects, ideas, experiments, decisions, research, learning,  |  |
|  |         opportunities, knowledge_edges, activity_logs                       |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 2. Component Design

### 2.1 Backend Services
1. **Database & Connection Manager (`app/database.py`)**:
   - Manages SQLite connection with Write-Ahead Logging (`WAL`), strict foreign keys (`PRAGMA foreign_keys = ON`), and thread-safe row factories.
   - Automatically migrates schema and seeds baseline demonstration data if the database is newly initialized.
2. **Domain Repository (`app/repository.py`)**:
   - Encapsulates database operations for all 8 primary domain entities.
   - Implements transactional integrity and updates knowledge edges atomically.
3. **Knowledge Graph Service (`app/graph_service.py`)**:
   - Traverses typed relational edges (`leads_to`, `validates`, `informs`, `implements`, `spawns`, `depends_on`, `references`).
   - Generates node clusters, adjacency sets, and formatted payloads for the frontend visual graph.
4. **Universal Search Service (`app/search_service.py`)**:
   - Executes multi-field, multi-entity unified queries with facet filters (entity type, status, priority, tags, date ranges).
5. **Grounded AI Studio Engine (`app/ai_service.py`)**:
   - Implements both deterministic rule-based analysis and dynamic LLM orchestration via `google-genai` / Vertex AI.
   - Strictly enforces truth boundaries using the 4-bracket taxonomy: `[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, and `[AI RECOMMENDATION]`.
6. **Situational Metrics Engine (`app/metrics_service.py`)**:
   - Computes real-time health distributions, backlog velocity, idea conversion funnel drop-offs, and projects with inactivity >14 days.

### 2.2 Frontend HUD Architecture
- **Single-Page Vanilla ES Module Architecture**: Zero heavy bundler dependencies; boots instantly in any modern browser.
- **Visual Graph Visualizer**: SVG-based force-directed node-link network with pan, zoom, click-to-focus, and edge labels.
- **Command Palette & Keyboard Handlers**:
  - `Cmd+K` / `Ctrl+K` / `/`: Opens Omni-Search.
  - `C`: Triggers Quick Capture modal.
  - `B`: Generates instant Grounded Daily Briefing.
  - `1`-`9`: Instant switch across HUD views.
  - `Esc`: Dismisses any active drawer or modal.

---

## 3. Security, Privacy & Reliability
- **Local Sovereignty**: All personal data is held locally on the user's disk in SQLite. No third-party analytics, tracking, or telemetry.
- **Zero Hallucination AI Guardrails**: The AI engine never invents facts or deadlines. Missing information is explicitly identified as an informational gap.
- **Input Validation**: All payloads validated using Pydantic v2 schemas with comprehensive typing.
