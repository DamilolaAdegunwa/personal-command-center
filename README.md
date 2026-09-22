# 🛰️ Personal Command Center (Personal OS)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-WAL%20Mode-003B57.svg?style=flat&logo=sqlite)](https://sqlite.org)
[![Test Suite](https://img.shields.io/badge/Tests-17%20Passed-emerald.svg?style=flat)](tests/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](LICENSE)

> A serious, local-first **Personal Operating System for an individual human being living and working in the AI era**. It transforms scattered notes, tasks, ideas, decisions, and research into **continuous situational awareness and actionable intelligence**.

---

## 1. Why This Exists: Beyond Generic Productivity Apps

Modern high-velocity builders, AI researchers, and technical founders suffer from **cognitive fragmentation and intelligence decay**:
- **Information Silos**: Tasks are isolated from projects, research papers sit unread in folders, ideas vanish into forgotten notes, and architectural decisions are made without capturing the assumptions behind them.
- **Passive Logging vs. Situational Posture**: Standard to-do apps are dumb lists. They don't know *why* you are doing a task, what *experiment* validates the underlying hypothesis, or how a recent *decision* impacted delivery.
- **Decision Amnesia**: High-stakes engineering and career choices are forgotten. Months later, when outcomes arrive, there is no retrospective audit trail to evaluate whether your confidence was calibrated.
- **Superficial "AI Chatbots"**: Typical AI productivity apps wrap arbitrary chatbots that hallucinate personal commitments.

**Personal Command Center** solves this with a cohesive, local-first personal OS that enforces relational links between **Ideas ➔ Research ➔ Experiments ➔ Decisions ➔ Projects ➔ Outcomes**, powered by a strictly grounded AI layer.

---

## 2. Architecture & Design Principles

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

### Key Technical Pillars
1. **Local Sovereignty & Speed**: Built on Python 3.14 + FastAPI + SQLite with Write-Ahead Logging (`WAL`). Sub-millisecond queries, zero background daemon baggage, effortlessly portable via a single `.db` file.
2. **Keyboard-Driven Cockpit**: Tactical dark HUD aesthetic with keyboard shortcuts (`Cmd+K` Omni-Search, `C` Quick Capture, `B` Daily Briefing, `1`-`9` Tab Switching).
3. **Zero-Hallucination Grounding**: Every AI analysis categorizes insights into `[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, and `[AI RECOMMENDATION]`.
4. **Relational Knowledge Graph**: Interactive SVG network visualizing how thoughts translate into real-world outcomes.

---

## 3. Core Modules & Capabilities

### 🎯 1. Today Cockpit
High-level tactical morning view:
- **Critical Fire Drills (P0)**: Urgent tasks requiring immediate deep-work intervention.
- **Active Deadlines**: Items due within the 72-hour horizon.
- **Dependency Blockers**: Escalated alerts with explicit blocker reasons and unblock controls.
- **Unfinished Work Units**: Clean scheduled tasks with energy-level categorization (`deep_work`, `quick_win`, `administrative`).

### 📁 2. Strategic Project Portfolio
Manage projects across 5 domains (`ai_systems`, `research`, `product`, `career`, `infrastructure`):
- Real-time health indicators: **Green** (on track), **Yellow** (risk/drift), **Red** (critical block).
- Progress percentage visualizer and target delivery dates.
- Explicit **Next Actions** breakdown.
- AI Project Diagnostic trigger.

### 💡 3. Idea Lifecycle Pipeline (Stage Machine)
Raw sparks move through 7 formal state gates:
```
Captured ➔ Explored ➔ Validated ➔ Planned ➔ Executing ➔ Completed / Abandoned
```
- Track origin, priority, and next validation action.
- Directly trigger **Idea Adversarial Stress-Tests** to expose unvalidated assumptions.

### 🧪 4. Empirical Experiments Engine
Transforms ideas into structured falsifiable science:
- Fields: **Hypothesis** (*"If X, then Y because Z"*), **Objective**, **Assumptions**, **Design**, **Expected Result**, **Empirical Evidence**, and **Conclusion**.
- Enforces an iterative loop: `Idea ➔ Hypothesis ➔ Experiment ➔ Evidence ➔ Decision ➔ Action`.

### ⚖️ 5. Decision Intelligence Log
A personal decision-making database to eliminate cognitive bias and decision amnesia:
- Records: Decision statement, date, driving context, alternatives considered with pros/cons, stated assumptions, evidence base, expected outcome, and confidence score (1-100%).
- Post-decision retrospective: Logs actual outcome and meta-lessons.
- Answer questions like: *"What decisions did I make last quarter, and how accurate was my confidence?"*

### 🔬 6. Deep Research Dossiers
Structured technical and market research:
- Captures research questions, investigative logs, verified findings with evidence citations, sources, conclusions, and unresolved questions.

### 📚 7. Learning & Skills Curriculum
Track technical mastery without passive bookmarking:
- Subjects, courses, books, tutorials, progress percentages.
- Practical exercises tracking (completed vs. pending).
- Core takeaway distillation.

### 🔭 8. Asymmetric Opportunity Radar
Proactively evaluate high-leverage opportunities:
- Categorized across career, business, tech, venture, investment, and partnerships.
- Captures potential upside, entry requirements, and risk factors.
- Structured so you can decide rationally without premature dismissal or FOMO.

### 🕸️ 9. Interactive Personal Knowledge Graph
Visual SVG network of relationships:
- Maps `Idea ➔ Research ➔ Finding ➔ Decision ➔ Project ➔ Opportunity`.
- Filter nodes by category, pan, zoom, and inspect node metadata in a sliding drawer.

### 🔍 10. Universal Omni-Search (`Cmd+K`)
Instantaneous unified search across all 8 entity tables:
- Token-scoring engine with faceted type badges, snippets, and instant navigation.

### ⚡ 11. Grounded AI Intelligence Studio
5 dedicated intelligence workflows:
1. **Daily Briefing**: 60-second morning situational digest of priorities, fire drills, and execution order.
2. **Weekly Review**: Retrospective of closed loops, friction points, and learning pace.
3. **Project Diagnostic**: Deep audit identifying missing information, schedule creep, and dependency bottlenecks.
4. **Idea Stress-Test**: Adversarial deconstruction of assumptions and validation test design.
5. **Decision Audit**: Calibration comparison between predicted confidence and actual recorded outcomes.

### 📊 12. Situational Awareness Metrics
Meaningful situational awareness metrics:
- Active vs. completed project velocity.
- Health distribution (Green / Yellow / Red).
- Idea conversion funnel rates.
- **Stagnation Radar**: Automated alerts for projects with zero activity >14 days or red health.

---

## 4. Project Structure

```
personal-command-center/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & REST route definitions
│   ├── database.py          # SQLite connection, WAL mode & schema migrations
│   ├── models.py            # Pydantic v2 domain schemas & enums
│   ├── repository.py        # Relational CRUD & edge management layer
│   ├── graph_service.py     # Knowledge graph node/edge resolution
│   ├── search_service.py    # Universal multi-entity omni-search
│   ├── metrics_service.py   # Situational metrics & stagnation engine
│   ├── ai_service.py        # Grounded AI studio (Gemini / Heuristic fallback)
│   └── seed_data.py         # Realistic domain demonstration data
├── static/
│   ├── index.html           # Command center HTML5 HUD interface
│   ├── css/
│   │   └── style.css        # Tactical dark command-center aesthetic
│   └── js/
│       ├── api.js           # REST API client
│       ├── graph.js         # Interactive SVG knowledge graph visualizer
│       └── app.js           # State management & keyboard shortcuts
├── docs/
│   ├── PRODUCT_SPECIFICATION.md  # Formal 12-section product specification
│   ├── ARCHITECTURE.md           # Systems architecture & security design
│   ├── DATA_MODEL.md             # Schema definitions & relationship topology
│   ├── AI_WORKFLOWS.md           # Grounding rules & prompt engineering
│   └── ROADMAP.md                # Future evolutionary horizons
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest path configuration
│   ├── test_api.py          # Comprehensive domain & CRUD test suite
│   └── test_ai_workflows.py # Grounding & AI synthesis verification
├── Makefile                 # Developer build & run tasks
├── run.sh                   # Instant launch script
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
└── README.md                # Flagship project documentation
```

---

## 5. Quickstart & Installation

### Prerequisites
- Python 3.11+ (Python 3.14 recommended)
- Modern web browser (Chrome, Safari, Firefox, Edge)

### Launch in 30 Seconds

```bash
# 1. Clone repository
git clone https://github.com/DamilolaAdegunwa/personal-command-center.git
cd personal-command-center

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Command Center
./run.sh
# or: make run
```

Open your browser to: **`http://127.0.0.1:8000`**  
Interactive OpenAPI documentation: **`http://127.0.0.1:8000/docs`**

---

## 6. Testing & Quality Gate

Run the automated test suite with pytest:

```bash
make test
# or: PYTHONPATH=. pytest -v tests/
```

### Test Coverage Summary:
- `test_api.py`: Full CRUD for all 8 entities, search queries, knowledge graph generation, metrics, and state transitions.
- `test_ai_workflows.py`: Validates presence of `[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, and `[AI RECOMMENDATION]` tags.

---

## 7. Keyboard Shortcuts Guide

| Keybinding | Action |
|---|---|
| `Cmd + K` or `/` | Open Universal Omni-Search |
| `C` | Open Quick Capture Drawer |
| `B` | Generate Grounded Tactical Daily Briefing |
| `1` | Switch to Today Cockpit |
| `2` | Switch to Projects Portfolio |
| `3` | Switch to Ideas Pipeline |
| `4` | Switch to Experiments |
| `5` | Switch to Decision Intelligence Log |
| `6` | Switch to Deep Research Dossiers |
| `7` | Switch to Skills & Learning Curriculum |
| `8` | Switch to Opportunity Radar |
| `9` | Switch to Knowledge Graph |
| `Esc` | Dismiss active modal, drawer, or search |

---

## 8. License

MIT License. Crafted with Google Antigravity for high-velocity builders in the AI era.
