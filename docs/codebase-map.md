# Codebase Map & Repository Anatomy

This document provides a comprehensive structural guide to the **Personal Command Center** codebase, explaining the role, responsibility, exported interfaces, and dependencies of every module.

---

## 1. Directory Tree Overview

```
personal-command-center/
├── app/                        # Python FastAPI backend application package
│   ├── ai_service.py           # Grounded AI studio engine & Gemini fallback
│   ├── database.py             # SQLite connection management & DDL schema
│   ├── graph_service.py        # Knowledge graph synthesis & edge resolution
│   ├── main.py                 # FastAPI application router & lifespan hooks
│   ├── metrics_service.py      # Telemetry, velocity & stagnation algorithms
│   ├── models.py               # Pydantic v2 domain schemas & enumerations
│   ├── repository.py           # Data access layer (CRUD SQL queries)
│   ├── search_service.py       # Universal omni-search token matching engine
│   └── seed_data.py            # Baseline demonstration domain records
├── static/                     # Vanilla ES6 client frontend HUD assets
│   ├── css/
│   │   └── style.css           # Tactical dark HUD styling & responsive grid
│   ├── js/
│   │   ├── api.js              # REST client wrapper & fetch helpers
│   │   ├── app.js              # UI controller, state manager & hotkeys
│   │   └── graph.js            # SVG force-directed knowledge graph renderer
│   └── index.html              # Single-page HTML5 HUD shell & modals
├── tests/                      # Automated test suite (Pytest)
│   ├── conftest.py             # Pytest fixtures & path configuration
│   ├── test_ai_workflows.py    # Grounding tags & AI synthesis assertions
│   └── test_api.py             # Full API CRUD & lifecycle test coverage
├── docs/                       # Complete engineering documentation portal
├── scripts/                    # Documentation validation & CI automation
├── Makefile                    # Standard engineering shortcuts (run, test, seed)
├── run.sh                      # Shell bootstrap script with auto-reload
├── requirements.txt            # Python runtime & test dependencies
├── pytest.ini                  # Pytest configuration file
├── personal_os.db              # SQLite persistent database (WAL mode)
└── README.md                   # Project landing page & documentation gateway
```

---

## 2. Backend Modules (`app/`)

### `app/main.py`
- **Architectural Role:** Central application controller.
- **Responsibilities:** Configures FastAPI app, registers lifespan manager (`init_db`, `seed_database`), mounts `/static`, and defines 24 REST endpoints.
- **Dependencies:** `fastapi`, `app.database`, `app.repository`, `app.models`, `app.ai_service`, `app.graph_service`, `app.search_service`, `app.metrics_service`, `app.seed_data`.

### `app/database.py`
- **Architectural Role:** Persistence and connection factory.
- **Responsibilities:** Manages SQLite connection pooling, enforces `PRAGMA journal_mode = WAL`, `PRAGMA foreign_keys = ON`, `PRAGMA busy_timeout = 5000`, and executes schema DDL migrations.
- **Exported Symbols:** `get_connection()`, `init_db()`, `DB_PATH`.

### `app/models.py`
- **Architectural Role:** Domain schema and type definitions.
- **Responsibilities:** Declares 17 Pydantic schemas and 17 enum types. Enforces data validation rules, defaults, and boundary constraints.
- **Exported Symbols:** `Task`, `Project`, `Idea`, `Experiment`, `Decision`, `ResearchEntry`, `LearningItem`, `Opportunity`, `KnowledgeEdge`, etc.

### `app/repository.py`
- **Architectural Role:** Data access object (DAO).
- **Responsibilities:** Encapsulates all SQL statements for CRUD operations on tasks, projects, ideas, experiments, decisions, research, learning, opportunities, and explicit edges. Generates UUIDs and ISO-8601 timestamps.
- **Exported Symbols:** `Repository` class with static CRUD methods.

### `app/ai_service.py`
- **Architectural Role:** Cognitive intelligence engine.
- **Responsibilities:** Gathers ground-truth context from `Repository`, invokes `gemini-2.5-flash` via `google-genai` if `GEMINI_API_KEY` is present, or falls back to a deterministic rule engine. Enforces the 4-bracket grounding taxonomy.
- **Exported Symbols:** `AIService` class (`generate_daily_briefing`, `generate_weekly_review`, `analyze_project`, `analyze_idea`, `review_decision`).

### `app/graph_service.py`
- **Architectural Role:** Knowledge graph topology constructor.
- **Responsibilities:** Traverses all entities, extracts implicit foreign key edges, merges explicit edges from `knowledge_edges`, deduplicates nodes/edges, and packages `GraphData`.
- **Exported Symbols:** `GraphService.get_full_graph()`.

### `app/search_service.py`
- **Architectural Role:** Multi-entity omni-search engine.
- **Responsibilities:** Tokenizes search queries, matches against 8 entity collections, computes relevance scores, applies filters, and returns ranked snippets.
- **Exported Symbols:** `SearchService.search()`.

### `app/metrics_service.py`
- **Architectural Role:** Situational awareness telemetry engine.
- **Responsibilities:** Computes health distributions, overdue commitments, idea conversion funnel velocity, and emits stagnation alerts for blocked items.
- **Exported Symbols:** `MetricsService.get_metrics()`.

### `app/seed_data.py`
- **Architectural Role:** Demonstration data generator.
- **Responsibilities:** Populates rich, realistic domain entities (4 projects, 4 ideas, 4 experiments, 4 decisions, research, learning, opportunities, and explicit edges) if the database is unseeded.
- **Exported Symbols:** `seed_database()`.

---

## 3. Frontend Modules (`static/`)

### `static/index.html`
- **Role:** DOM skeleton for the Single-Page Application.
- **Components:** Top Tactical Bar, Left Navigation Sidebar, Dynamic Viewport (10 tab views), Quick Capture Drawer, Omni-Search Modal, Toast Container.

### `static/css/style.css`
- **Role:** Visual design system.
- **Features:** CSS variables for dark HUD theme, fluid CSS grid, glowing status indicators, responsive drawers.

### `static/js/api.js`
- **Role:** REST API client.
- **Features:** Handles asynchronous `fetch` calls, status validation, and error toast triggers.

### `static/js/app.js`
- **Role:** Frontend state controller and event coordinator.
- **Features:** View routing, tab switching, global keyboard shortcuts (`Cmd+K`, `C`, `B`, `1-9`), form submissions.

### `static/js/graph.js`
- **Role:** Interactive SVG knowledge graph visualizer.
- **Features:** Dynamic force-directed node positioning, SVG path curves, node dragging, click-to-focus inspectors.

---

## 4. Test Modules (`tests/`)

### `tests/conftest.py`
- Adds repository root to `sys.path` to ensure clean imports during pytest execution.

### `tests/test_api.py`
- Contains 12 integration tests verifying health checks, CRUD operations, state machines, and omni-search.

### `tests/test_ai_workflows.py`
- Contains 5 tests asserting strict grounding markers (`[FACT]`, `[AI RECOMMENDATION]`) and accurate context reflection.
