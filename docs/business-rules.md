# Business Rules Catalog & Domain Logic

This document catalogs the operational business rules, state machine transitions, and computational heuristics discovered across the **Personal Command Center** implementation.

---

## 1. Summary of Business Rules

| Rule ID | Rule Title | Primary Implementation Location | Enforcing Mechanism |
|---|---|---|---|
| **BR-01** | Task Completion Timestamp Tracking | `app/repository.py` (`update_task`, `create_task`) | Repository DAO logic |
| **BR-02** | 7-Stage Idea State Progression | `app/main.py` (`transition_idea`), `app/models.py` | State machine API & Schema |
| **BR-03** | 4-Bracket AI Grounding Taxonomy | `app/ai_service.py` (All AI workflows) | Prompt engineering & Heuristics |
| **BR-04** | P0 Critical Fire-Drill Prioritization | `app/repository.py` (`get_tasks`), `app/main.py` | SQL `CASE` ordering & filtering |
| **BR-05** | 14-Day Project Stagnation Alert | `app/metrics_service.py` (`get_metrics`) | Temporal diff & health check |
| **BR-06** | 72-Hour Approaching Deadline Window | `app/main.py` (`get_today`), `app/ai_service.py` | Datetime horizon arithmetic |
| **BR-07** | Decision Review Due Trigger | `app/metrics_service.py` (`get_metrics`) | Target date threshold comparison |
| **BR-08** | Automatic Implicit Edge Resolution | `app/graph_service.py` (`get_full_graph`) | Foreign key relationship traversal |
| **BR-09** | Omni-Search Relevance Weighting | `app/search_service.py` (`match_score`) | Token scoring algorithm |

---

## 2. In-Depth Rule Specifications

### BR-01: Task Completion Timestamp Tracking
- **Statement:** When a task enters the `completed` state, its `completed_at` field must be stamped with the current UTC ISO-8601 timestamp. If a completed task is moved back to an active state (`todo`, `in_progress`, `blocked`), `completed_at` must be reset to `NULL`.
- **Implementation:** `app/repository.py` lines 92 and 120-123.
- **Trigger:** Invocation of `create_task` with `status=completed` or `update_task` with modified status.
- **Relevant Tests:** `tests/test_api.py::test_projects_crud`

### BR-02: 7-Stage Idea State Progression
- **Statement:** Ideas progress through a formal 7-stage lifecycle:
  ```
  captured ➔ explored ➔ validated ➔ planned ➔ executing ➔ completed / abandoned
  ```
  Every state transition must update the `status_changed_at` timestamp.
- **Implementation:** `app/main.py` (`transition_idea`), `app/models.py` (`IdeaStatus`).
- **Trigger:** Calling `POST /api/ideas/{id}/transition?target_status=...`.
- **Relevant Tests:** `tests/test_api.py::test_ideas_lifecycle_state_machine`.

### BR-03: 4-Bracket AI Grounding Taxonomy
- **Statement:** Every synthesized AI output must categorize its statements into four explicit bracket tags:
  1. `[FACT]`: Verifiable ground-truth data from the database.
  2. `[USER CONTEXT]`: Explicit rationales, descriptions, or notes recorded by the user.
  3. `[ASSUMPTION]`: Deduced risks, missing dates, or untested variables.
  4. `[AI RECOMMENDATION]`: Tactical prioritization proposals.
  No statement may be output without an explicit grounding tag.
- **Implementation:** `app/ai_service.py` (system instructions and deterministic fallback rules).
- **Relevant Tests:** `tests/test_ai_workflows.py::test_daily_briefing_grounding`, `tests/test_ai_workflows.py::test_weekly_review_grounding`.

### BR-04: P0 Critical Fire-Drill Prioritization
- **Statement:** Tasks are prioritized in strict ordinal rank: `p0_critical` (Rank 0) > `p1_high` (Rank 1) > `p2_medium` (Rank 2) > `p3_low` (Rank 3). Within each priority tier, tasks with earlier deadlines appear first.
- **Implementation:** `app/repository.py` (`get_tasks` SQL `ORDER BY CASE priority ...`).
- **Trigger:** Standard task listing in the Today cockpit.
- **Relevant Tests:** `tests/test_api.py::test_today_dashboard`.

### BR-05: 14-Day Project Stagnation Alert
- **Statement:** An active project is flagged as "stalled" and generates an urgent stagnation alert if its `health` is `red` or if its `updated_at` timestamp is older than 14 days (`now - 14 days`).
- **Implementation:** `app/metrics_service.py` lines 22-29 and 86-92.
- **Trigger:** Polling `/api/metrics`.
- **Relevant Tests:** `tests/test_api.py::test_situational_metrics`.

### BR-06: 72-Hour Approaching Deadline Window
- **Statement:** Incomplete tasks whose deadline falls within the upcoming 72 hours (3.0 days) are categorized as "approaching deadlines" and highlighted in the Today cockpit and Daily Briefing.
- **Implementation:** `app/ai_service.py` lines 44-55, `app/main.py` lines 82-84.
- **Trigger:** Calculation of daily briefing and dashboard metrics.

### BR-07: Decision Review Due Trigger
- **Statement:** A logged decision in `pending_review` status whose `review_date` is less than or equal to the current UTC date emits a `decision_review_due` stagnation alert in the metrics telemetry.
- **Implementation:** `app/metrics_service.py` lines 100-112.
- **Trigger:** Polling `/api/metrics`.
- **Relevant Tests:** `tests/test_api.py::test_situational_metrics`.

### BR-08: Automatic Implicit Edge Resolution
- **Statement:** Relational foreign keys across entities automatically generate directed semantic graph edges:
  - Idea with `related_project_id` ➔ spawns `(Idea, Project, 'spawns')`
  - Experiment with `idea_id` ➔ spawns `(Idea, Experiment, 'validates')`
  - Experiment with `project_id` ➔ spawns `(Experiment, Project, 'informs')`
  - Research with `related_project_id` ➔ spawns `(Research, Project, 'informs')`
- **Implementation:** `app/graph_service.py` lines 41-51, 66-87, 116-126.
- **Relevant Tests:** `tests/test_api.py::test_knowledge_graph_data`.

### BR-09: Omni-Search Relevance Weighting
- **Statement:** In-memory keyword search computes relevance scores:
  - Query token appears in title: `+5.0` points
  - Query token appears in description / snippet: `+1.5` points
  - Entity is a Project: `+1.0` boost point
  Results are sorted descending by score and capped at `limit` (default 40).
- **Implementation:** `app/search_service.py` lines 18-29 and 217.
- **Relevant Tests:** `tests/test_api.py::test_universal_omni_search`.
