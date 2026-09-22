# 🛰️ Personal Command Center (Personal OS)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.14+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-WAL%20Mode-003B57.svg?style=flat&logo=sqlite)](https://sqlite.org)
[![Documentation](https://img.shields.io/badge/Docs-Enterprise%20Portal-blueviolet.svg?style=flat)](docs/README.md)
[![Test Suite](https://img.shields.io/badge/Tests-18%20Passed-emerald.svg?style=flat)](tests/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat)](LICENSE)

> A serious, local-first **Personal Operating System for an individual human being living and working in the AI era**. It transforms scattered notes, tasks, ideas, decisions, and research into **continuous situational awareness and actionable intelligence**.

---

## 1. Project Purpose

High-velocity builders, technical founders, and AI researchers suffer from **cognitive fragmentation and intelligence decay**:
- **Information Silos:** Tasks live in to-do lists, ideas in notes apps, papers in browser tabs, and decisions in chat logs.
- **Decision Amnesia:** Critical architectural and career choices are made on unrecorded assumptions without a retrospective audit trail.
- **Idea Graves:** Creative sparks rarely reach empirical validation or project execution.
- **Superficial AI Wrappers:** Most productivity tools wrap generic LLMs that hallucinate personal commitments.

**Personal Command Center** solves this through a local-first, low-latency personal operating system that enforces relational connections across:
```
Ideas ➔ Empirical Experiments ➔ Strategic Decisions ➔ Execution Projects ➔ Concrete Tasks
```
Every AI synthesis is anchored in verified local database records using a strict **4-bracket truth taxonomy** (`[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, `[AI RECOMMENDATION]`).

---

## 2. Architecture & System Summary

```
+-----------------------------------------------------------------------------------+
|                                CLIENT FRONTEND                                    |
|  +------------------+  +-------------------+  +--------------------------------+  |
|  | Tactical HUD View|  | Interactive SVG   |  | Universal Omni-Search (Cmd+K)  |  |
|  | (10 Core Modules)|  | Knowledge Graph   |  | Faceted Filtering Engine       |  |
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
|  | (24 Endpoints)    |  | Engine (Token-Based)|  | (Node & Edge Synthesizer)   |  |
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
|  | 9 Tables: tasks, projects, ideas, experiments, decisions, research,       |  |
|  |           learning, opportunities, knowledge_edges                          |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Technology Stack

- **Backend Runtime:** Python 3.14+
- **Application Framework:** FastAPI 0.115+
- **ASGI Web Server:** Uvicorn 0.30+
- **Persistence:** SQLite 3.50+ (Write-Ahead Logging mode, foreign key cascades)
- **Validation & Typing:** Pydantic v2.8+
- **Frontend HUD:** Pure Vanilla HTML5, CSS3 Variables, ES6 Modules, and Native SVG (Zero Node.js or npm dependencies)
- **AI Intelligence:** Google GenAI SDK (`gemini-2.5-flash`) with deterministic local heuristic fallback
- **Test Automation:** Pytest 8.0+ and HTTPX

---

## 4. Repository Structure

```
personal-command-center/
├── app/                  # Backend application package (FastAPI, Repository, Services)
├── static/               # Client frontend HUD (Vanilla ES6, CSS, SVG Graph)
├── tests/                # Automated test suite (18 integration & AI tests)
├── docs/                 # Enterprise documentation portal (17+ technical areas)
├── scripts/              # Documentation and release automation scripts
├── Makefile              # Engineering shortcuts (run, test, seed, clean)
├── run.sh                # Shell bootstrap script with auto-reload
├── requirements.txt      # Python dependencies
├── pytest.ini            # Test runner configuration
└── personal_os.db        # SQLite database (auto-created upon startup)
```

---

## 5. Quick Start

### 5.1 Launching the Command Center
In your terminal, simply execute:
```bash
./run.sh
```
Or using Make:
```bash
make run
```
The server will boot on `http://127.0.0.1:8000`. Demonstrating data is seeded automatically if the database is uninitialized.

### 5.2 Keyboard Shortcuts (Cockpit HUD)
- `Cmd+K` / `Ctrl+K`: Universal Omni-Search across all entities
- `C`: Quick Capture modal (Task, Idea, Project, Decision)
- `B`: Generate Grounded Daily Briefing
- `1` - `9`: Instant switch across HUD views
- `Esc`: Dismiss drawer or modal

---

## 6. Complete Documentation Portal (`docs/`)

The repository includes a comprehensive, modular documentation portal:

| Documentation Domain | Path | Description |
|---|---|---|
| **Portal Home** | [docs/README.md](docs/README.md) | Central entry point and role-based reading tracks |
| **Master Index** | [docs/index.md](docs/index.md) | Deep links to all 20+ documentation artifacts |
| **System Architecture** | [docs/architecture/](docs/architecture/index.md) | System topology, component dependencies, and data flows |
| **REST API Reference** | [docs/api/](docs/api/index.md) | Complete documentation of all endpoints and Pydantic schemas |
| **Developer Guide** | [docs/development/](docs/development/index.md) | Prerequisites, local setup, workflows, and conventions |
| **Configuration Reference**| [docs/configuration/](docs/configuration/index.md) | Environment variables, defaults, and sensitivity catalog |
| **Database & Storage** | [docs/database/](docs/database/index.md) | SQLite WAL mode, schema specifications, and ER diagram |
| **External Integrations**| [docs/integrations/](docs/integrations/index.md) | Google Gemini API integration and MCP roadmap |
| **Messaging & Events** | [docs/messaging/](docs/messaging/index.md) | Synchronous execution model and future async event bus |
| **Testing Guide** | [docs/testing/](docs/testing/index.md) | Test suite breakdown, execution, and fixture patterns |
| **Deployment Guide** | [docs/deployment/](docs/deployment/index.md) | Standalone process, launchd daemon, and Docker blueprints |
| **Operations Runbook** | [docs/operations/runbook.md](docs/operations/runbook.md) | Production operations, health probes, backups, and recovery |
| **Troubleshooting Guide**| [docs/operations/troubleshooting.md](docs/operations/troubleshooting.md) | Matrix of symptoms, causes, diagnostics, and resolutions |
| **Security & Privacy** | [docs/security/](docs/security/index.md) | Threat model, local sovereignty, and formal security review |
| **Business Rules Catalog** | [docs/business-rules.md](docs/business-rules.md) | Formal catalog of 9 domain rules and state machine triggers |
| **Codebase Map** | [docs/codebase-map.md](docs/codebase-map.md) | Detailed file-by-file responsibility guide |
| **Domain Glossary** | [docs/glossary.md](docs/glossary.md) | Definitions for 40+ domain and technical terms |
| **Engineering FAQ** | [docs/faq.md](docs/faq.md) | Role-specific inquiries for developers, architects, and DevOps |
| **Traceability Matrix** | [docs/documentation-traceability.md](docs/documentation-traceability.md) | Source code line mapping with confidence ratings |
| **Documentation Policy** | [docs/documentation-maintenance.md](docs/documentation-maintenance.md) | Change management guidelines and PR checklists |
| **Audit & Changelog** | [docs/DOCUMENTATION-AUDIT.md](docs/DOCUMENTATION-AUDIT.md) | Initial audit findings, completeness matrix, and changelog |

---

## 7. Testing & Verification

Run the automated test suite covering all APIs, AI grounding rules, and documentation integrity:
```bash
PYTHONPATH=. pytest -v tests/
```
To validate documentation link integrity and endpoint parity independently:
```bash
python3 scripts/validate_docs.py
```

---

## 8. License

This software is released under the [MIT License](LICENSE).
