# Testing & Verification Documentation

This document describes the automated testing framework, test suite architecture, fixture patterns, and coverage analysis for the **Personal Command Center**.

---

## 1. Testing Strategy & Philosophy

The testing architecture prioritizes **real-world integration and regression defense**:
- **End-to-End API Integration:** Tests execute against real FastAPI routes using `fastapi.testclient.TestClient`.
- **Real Database Transactions:** Tests interact with the actual SQLite engine and relational schema rather than superficial mock objects, guaranteeing SQL compatibility and foreign key cascade verification.
- **Strict Grounding Assertions:** Tests in `tests/test_ai_workflows.py` assert that synthesized AI outputs strictly contain verified grounding markers (`[FACT]`, `[AI RECOMMENDATION]`).

---

## 2. Test Suite Catalog

The codebase currently contains **17 verified automated tests** divided across two test modules:

### 2.1 `tests/test_api.py` (12 Tests)
| Test Function | Verification Scope | Target Endpoint |
|---|---|---|
| `test_healthcheck` | Liveness probe and version envelope | `GET /api/health` |
| `test_today_dashboard` | Critical P0, blocked items, and deadline aggregation | `GET /api/today` |
| `test_projects_crud` | Full Create, Read, Update, Delete project lifecycle | `/api/projects/*` |
| `test_ideas_lifecycle_state_machine` | 7-stage state transitions (`captured` ➔ `executing`) | `/api/ideas/*` |
| `test_experiments_workflow` | Hypothesis creation, evidence recording, conclusion | `/api/experiments/*` |
| `test_decisions_intelligence` | Structured decision logging and confidence calibration | `/api/decisions/*` |
| `test_research_entries` | Dossier logging, findings arrays, sources, questions | `/api/research/*` |
| `test_learning_items` | Curriculum tracking and practical exercise completion | `/api/learning/*` |
| `test_opportunity_radar` | Upside evaluation, risk scoring, status updates | `/api/opportunities/*` |
| `test_universal_omni_search` | Multi-entity token matching and relevance scoring | `GET /api/search` |
| `test_knowledge_graph_data` | Node deduplication and implicit edge resolution | `GET /api/graph` |
| `test_situational_metrics` | Stagnation alert generation, overdue task calculations | `GET /api/metrics` |

### 2.2 `tests/test_ai_workflows.py` (5 Tests)
| Test Function | Verification Scope | Target Endpoint |
|---|---|---|
| `test_daily_briefing_grounding` | Grounding tags (`[FACT]`, `[REC]`) & real data matching | `POST /api/ai/daily-briefing` |
| `test_weekly_review_grounding` | 7-day retrospective synthesis and drag factor analysis | `POST /api/ai/weekly-review` |
| `test_project_diagnostic_audit` | Architectural trajectory and missing deadline warnings | `POST /api/ai/analyze-project/{id}` |
| `test_idea_stress_test` | Assumption deconstruction and experiment blueprints | `POST /api/ai/analyze-idea/{id}` |
| `test_decision_audit` | Calibration audit comparing expectation vs. actual outcome | `POST /api/ai/review-decision/{id}` |

---

## 3. Test Execution & Commands

### 3.1 Executing All Automated Tests
```bash
# Run pytest across all test files
PYTHONPATH=. pytest -v tests/
```

### 3.2 Running with Warning Filtering
```bash
# Suppress Starlette deprecation notices
PYTHONPATH=. pytest -v tests/ -W ignore::DeprecationWarning
```

### 3.3 Running by Target Module
```bash
PYTHONPATH=. pytest -v tests/test_api.py
PYTHONPATH=. pytest -v tests/test_ai_workflows.py
```

---

## 4. Test Fixtures & Isolation

Tests share a module-scoped fixture in `tests/conftest.py` and test modules:

```python
@pytest.fixture(scope="module")
def client():
    init_db()
    seed_database()
    with TestClient(app) as c:
        yield c
```

- **Database Pre-Condition:** `init_db()` ensures all tables exist, and `seed_database()` guarantees predictable baseline fixtures for reading tests.
- **Client Lifespan:** `with TestClient(app)` executes the FastAPI lifespan context manager, mirroring real production startup.

---

## 5. Identified Testing Gaps

The documentation audit identified the following areas that currently lack test coverage:
1. **Schema Validation Boundary Tests:** No tests currently verify that invalid enums (e.g. `status="invalid_status"`) or negative progress percentages (`progress_pct=-10`) properly return HTTP 422.
2. **Concurrent Database Access:** No stress tests currently simulate simultaneous write contention across threads to test the 5,000ms `busy_timeout`.
3. **Automated Documentation Parity Tests:** Handled in Phase 8 via `tests/test_docs_validation.py`.
