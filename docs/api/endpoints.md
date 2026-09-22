# REST API Endpoint Reference

This document provides exhaustive technical specifications for all endpoints exposed by the **Personal Command Center** backend.

---

## Table of Contents
1. [System & Health](#1-system--health)
2. [Today Cockpit](#2-today-cockpit)
3. [Strategic Projects](#3-strategic-projects)
4. [Idea Lifecycle Pipeline](#4-idea-lifecycle-pipeline)
5. [Empirical Experiments Engine](#5-empirical-experiments-engine)
6. [Decision Intelligence Log](#6-decision-intelligence-log)
7. [Research Dossiers](#7-research-dossiers)
8. [Continuous Learning Tracker](#8-continuous-learning-tracker)
9. [Opportunity Radar](#9-opportunity-radar)
10. [Commitments & Tasks](#10-commitments--tasks)
11. [Knowledge Graph & Edges](#11-knowledge-graph--edges)
12. [Universal Omni-Search](#12-universal-omni-search)
13. [Situational Awareness Metrics](#13-situational-awareness-metrics)
14. [Grounded AI Studio](#14-grounded-ai-studio)
15. [Data Seeding / Reset](#15-data-seeding--reset)

---

## 1. System & Health

### `GET /`
- **Purpose:** Serves the frontend single-page application entry point (`static/index.html`).
- **Response:** HTTP 200 with HTML stream, or JSON if static file is unbuilt.

### `GET /api/health`
- **Purpose:** Liveness and readiness health probe for automated monitoring.
- **Response Example (200 OK):**
  ```json
  {
    "status": "operational",
    "system": "Personal Command Center (Personal OS)",
    "version": "1.0.0"
  }
  ```

---

## 2. Today Cockpit

### `GET /api/today`
- **Purpose:** Aggregates tactical morning overview metrics, P0 fire drills, blocked items, and deadlines within 72 hours.
- **Response Structure (200 OK):**
  ```json
  {
    "summary": {
      "active_projects_count": 3,
      "p0_count": 1,
      "p1_count": 2,
      "blocked_count": 1,
      "in_progress_count": 2,
      "unfinished_total": 5
    },
    "critical_p0": [...],
    "high_priority_p1": [...],
    "blocked_items": [...],
    "active_work": [...],
    "upcoming_deadlines": [...],
    "active_projects": [...]
  }
  ```

---

## 3. Strategic Projects

### `GET /api/projects`
- **Purpose:** List projects matching optional filters.
- **Query Parameters:**
  - `status` (string, optional): `active`, `planned`, `completed`, `blocked`, `maintenance`
  - `health` (string, optional): `green`, `yellow`, `red`
- **Response:** `200 OK` `List[Project]`

### `POST /api/projects`
- **Purpose:** Register a new strategic project.
- **Request Body (`ProjectCreate`):**
  ```json
  {
    "title": "Quantum Memory Shm Engine",
    "description": "Ultra low latency inter-process communication",
    "category": "ai_systems",
    "status": "active",
    "health": "green",
    "progress_pct": 10,
    "next_actions": ["Write POSIX shm binding"],
    "target_date": "2026-11-15"
  }
  ```
- **Response:** `200 OK` `Project`

### `GET /api/projects/{project_id}`
- **Purpose:** Retrieve a single project by UUID.
- **Errors:** `404 Not Found` if `project_id` does not exist.

### `PUT /api/projects/{project_id}`
- **Purpose:** Update fields of an existing project.
- **Request Body (`ProjectUpdate`):** Any subset of `ProjectCreate` fields.
- **Response:** `200 OK` `Project`
- **Errors:** `404 Not Found`

### `DELETE /api/projects/{project_id}`
- **Purpose:** Remove a project. Associated tasks and ideas have `project_id` set to `NULL` (via SQLite foreign key cascade).
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 4. Idea Lifecycle Pipeline

### `GET /api/ideas`
- **Query Parameters:** `status` (`IdeaStatus`), `category` (`IdeaCategory`)
- **Response:** `200 OK` `List[Idea]`

### `POST /api/ideas`
- **Request Body (`IdeaCreate`):**
  ```json
  {
    "title": "Attention Head Sparsity Pruning",
    "description": "Prune redundant heads at inference",
    "category": "software",
    "origin": "Reading FlashAttention-3",
    "status": "captured",
    "priority": "high",
    "next_action": "Profile memory bandwidth",
    "related_project_id": null
  }
  ```
- **Response:** `200 OK` `Idea`

### `GET /api/ideas/{idea_id}`
- **Response:** `200 OK` `Idea`
- **Errors:** `404 Not Found`

### `PUT /api/ideas/{idea_id}`
- **Request Body (`IdeaUpdate`):** Subset of `IdeaCreate` fields.
- **Response:** `200 OK` `Idea`
- **Errors:** `404 Not Found`

### `POST /api/ideas/{idea_id}/transition`
- **Purpose:** Advances or alters an idea's stage in the 7-stage state machine. Updates `status_changed_at` timestamp.
- **Query Parameters:** `target_status` (`captured`, `explored`, `validated`, `planned`, `executing`, `completed`, `abandoned`).
- **Response:** `200 OK` `Idea`
- **Errors:** `404 Not Found`

### `DELETE /api/ideas/{idea_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 5. Empirical Experiments Engine

### `GET /api/experiments`
- **Query Parameters:** `status` (`hypothesis`, `design`, `running`, `analyzing`, `concluded`, `aborted`)
- **Response:** `200 OK` `List[Experiment]`

### `POST /api/experiments`
- **Request Body (`ExperimentCreate`):**
  ```json
  {
    "idea_id": "optional-uuid",
    "project_id": "optional-uuid",
    "title": "Attention Head Sparsity vs Perplexity",
    "hypothesis": "Dropping 40% of heads reduces memory by 30% with <0.1 perplexity loss",
    "objective": "Measure latency and perplexity on Wikitext-2",
    "assumptions": ["Heads can be identified by L1 norm"],
    "experiment_design": "Evaluate 100 test prompts with pruned masks",
    "expected_result": "Throughput increases by 1.4x",
    "status": "hypothesis"
  }
  ```
- **Response:** `200 OK` `Experiment`

### `GET /api/experiments/{exp_id}`
- **Response:** `200 OK` `Experiment`
- **Errors:** `404 Not Found`

### `PUT /api/experiments/{exp_id}`
- **Request Body (`ExperimentUpdate`):** Can include `actual_result`, `evidence`, `conclusion`, `next_step`, `status`.
- **Response:** `200 OK` `Experiment`
- **Errors:** `404 Not Found`

### `DELETE /api/experiments/{exp_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 6. Decision Intelligence Log

### `GET /api/decisions`
- **Query Parameters:** `status` (`pending_review`, `reviewed`, `superseded`)
- **Response:** `200 OK` `List[Decision]`

### `POST /api/decisions`
- **Request Body (`DecisionCreate`):**
  ```json
  {
    "title": "Migrate from REST to gRPC for Internal IPC",
    "date": "2026-09-22",
    "context": "Subagent processes require microsecond message passing",
    "alternatives_considered": [
      {"option": "gRPC", "pros": "Protobuf, streaming", "cons": "Schema overhead"},
      {"option": "REST JSON", "pros": "Simple", "cons": "Text serialization CPU"}
    ],
    "assumptions": "Message volume exceeds 500 msgs/sec",
    "evidence": "Microbenchmark showed JSON consumed 18% CPU",
    "expected_outcome": "p99 serialization latency under 0.2ms",
    "confidence_level": 88,
    "status": "pending_review",
    "review_date": "2026-10-22"
  }
  ```
- **Response:** `200 OK` `Decision`

### `GET /api/decisions/{dec_id}`
- **Response:** `200 OK` `Decision`
- **Errors:** `404 Not Found`

### `PUT /api/decisions/{dec_id}`
- **Request Body (`DecisionUpdate`):** Allows recording `actual_outcome`, `lessons_learned`, `status`.
- **Response:** `200 OK` `Decision`
- **Errors:** `404 Not Found`

### `DELETE /api/decisions/{dec_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 7. Research Dossiers

### `GET /api/research`
- **Query Parameters:** `topic` (string), `status` (`exploring`, `synthesizing`, `concluded`, `dormant`)
- **Response:** `200 OK` `List[ResearchEntry]`

### `POST /api/research`
- **Request Body (`ResearchEntryCreate`):**
  ```json
  {
    "research_question": "Can FlashDecoding support tree-structured candidates?",
    "topic": "Parallel LLM Decoding",
    "status": "exploring",
    "investigations": "Examining prefix tree caching in GPU shared memory",
    "findings": [
      {"claim": "Prefix sharing reduces redundant GEMV by 55%", "evidence": "CUDA simulation", "confidence": "high"}
    ],
    "sources": [
      {"title": "Flash-Decoding paper", "url_or_citation": "Dao et al., 2023", "type": "paper"}
    ],
    "conclusions": "Feasible with custom warp reduction",
    "unresolved_questions": ["Memory pressure under 128 candidates?"],
    "related_project_id": null
  }
  ```
- **Response:** `200 OK` `ResearchEntry`

### `GET /api/research/{res_id}`
- **Response:** `200 OK` `ResearchEntry`
- **Errors:** `404 Not Found`

### `PUT /api/research/{res_id}`
- **Response:** `200 OK` `ResearchEntry`
- **Errors:** `404 Not Found`

### `DELETE /api/research/{res_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 8. Continuous Learning Tracker

### `GET /api/learning`
- **Query Parameters:** `status` (`queued`, `active`, `paused`, `completed`)
- **Response:** `200 OK` `List[LearningItem]`

### `POST /api/learning`
- **Request Body (`LearningItemCreate`):**
  ```json
  {
    "subject": "GPU Architecture",
    "title": "CUDA Mode: Modern GPU Programming",
    "type": "course",
    "progress_pct": 65,
    "status": "active",
    "notes": "Covered warp synchronization and tensor cores",
    "practical_exercises": [
      {"title": "Implement FlashAttention-2 naive forward pass", "completed": true}
    ],
    "key_takeaways": "Memory bandwidth is the primary bottleneck"
  }
  ```
- **Response:** `200 OK` `LearningItem`

### `GET /api/learning/{item_id}`
- **Response:** `200 OK` `LearningItem`
- **Errors:** `404 Not Found`

### `PUT /api/learning/{item_id}`
- **Response:** `200 OK` `LearningItem`
- **Errors:** `404 Not Found`

### `DELETE /api/learning/{item_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 9. Opportunity Radar

### `GET /api/opportunities`
- **Query Parameters:** `category` (`OpportunityCategory`), `status` (`evaluating`, `pursuing`, `watching`, `archived`)
- **Response:** `200 OK` `List[Opportunity]`

### `POST /api/opportunities`
- **Request Body (`OpportunityCreate`):**
  ```json
  {
    "title": "Edge AI Inference Acceleration Grant",
    "description": "Compute grant offering $50k cloud H100 credits",
    "source": "Open-Source AI Foundation announcement",
    "date_discovered": "2026-09-18",
    "category": "technology",
    "potential_upside": "$50,000 compute credits",
    "requirements": "Working prototype and benchmark paper",
    "risks": "Exclusivity clause on pre-trained model weights",
    "status": "evaluating",
    "next_action": "Submit proposal before Oct 15"
  }
  ```
- **Response:** `200 OK` `Opportunity`

### `GET /api/opportunities/{opp_id}`
- **Response:** `200 OK` `Opportunity`
- **Errors:** `404 Not Found`

### `PUT /api/opportunities/{opp_id}`
- **Response:** `200 OK` `Opportunity`
- **Errors:** `404 Not Found`

### `DELETE /api/opportunities/{opp_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 10. Commitments & Tasks

### `GET /api/tasks`
- **Query Parameters:**
  - `status` (`todo`, `in_progress`, `blocked`, `completed`)
  - `priority` (`p0_critical`, `p1_high`, `p2_medium`, `p3_low`)
  - `project_id` (UUID string)
- **Response:** `200 OK` `List[Task]` (Sorted by priority ASC, deadline ASC, created_at DESC)

### `POST /api/tasks`
- **Request Body (`TaskCreate`):**
  ```json
  {
    "title": "Profile GPU kernel shared memory bank conflicts",
    "project_id": "optional-project-uuid",
    "status": "todo",
    "priority": "p1_high",
    "deadline": "2026-09-25T18:00:00",
    "scheduled_date": "2026-09-23",
    "blocker_reason": null,
    "energy_level": "deep_work",
    "tags": ["cuda", "performance"]
  }
  ```
- **Response:** `200 OK` `Task`

### `GET /api/tasks/{task_id}`
- **Response:** `200 OK` `Task`
- **Errors:** `404 Not Found`

### `PUT /api/tasks/{task_id}`
- **Purpose:** Updates task fields. When `status` transitions to `completed`, automatically sets `completed_at` timestamp.
- **Request Body (`TaskUpdate`):** Any subset of `TaskCreate` fields.
- **Response:** `200 OK` `Task`
- **Errors:** `404 Not Found`

### `DELETE /api/tasks/{task_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 11. Knowledge Graph & Edges

### `GET /api/graph`
- **Purpose:** Returns the complete graph topology including all nodes and combined explicit/implicit edges.
- **Response (200 OK):**
  ```json
  {
    "nodes": [
      {
        "id": "proj-1",
        "label": "Nexus Sovereign AI",
        "type": "project",
        "subtitle": "ai_systems • 78%",
        "status": "active",
        "health": "green",
        "data": { ... }
      }
    ],
    "edges": [
      {
        "id": "edge-idea1-proj1",
        "source": "idea-1",
        "target": "proj-1",
        "relation": "spawns",
        "notes": "Idea attached to project"
      }
    ]
  }
  ```

### `GET /api/edges`
- **Query Parameters:** `entity_type` (string), `entity_id` (string)
- **Response:** `200 OK` `List[KnowledgeEdge]`

### `POST /api/edges`
- **Request Body (`KnowledgeEdgeCreate`):**
  ```json
  {
    "source_type": "decision",
    "source_id": "dec-1",
    "target_type": "project",
    "target_id": "proj-1",
    "relation_type": "informs",
    "notes": "Architecture choice governs project runtime"
  }
  ```
- **Response:** `200 OK` `KnowledgeEdge`

### `DELETE /api/edges/{edge_id}`
- **Response:** `200 OK` `{"deleted": true}`
- **Errors:** `404 Not Found`

---

## 12. Universal Omni-Search

### `GET /api/search`
- **Query Parameters:**
  - `q` (string, required): Keyword tokens
  - `types` (list of strings, optional): `task`, `project`, `idea`, `experiment`, `decision`, `research`, `learning`, `opportunity`
  - `status` (string, optional)
  - `priority` (string, optional)
  - `tag` (string, optional)
  - `limit` (integer, default 40)
- **Response (200 OK):**
  ```json
  [
    {
      "id": "uuid",
      "entity_type": "research",
      "title": "Can FlashDecoding support tree candidates?",
      "subtitle": "Research • Topic: Parallel LLM Decoding • exploring",
      "status": "exploring",
      "snippet": "Prefix tree caching in GPU shared memory...",
      "relevance_score": 6.5
    }
  ]
  ```

---

## 13. Situational Awareness Metrics

### `GET /api/metrics`
- **Purpose:** Computes live organizational velocity, health distributions, and stagnation bottlenecks.
- **Response (200 OK):**
  ```json
  {
    "active_projects": 3,
    "completed_projects": 1,
    "stalled_projects": 1,
    "overdue_tasks": 1,
    "critical_p0_tasks": 1,
    "blocked_tasks": 1,
    "ideas_captured": 4,
    "ideas_validated": 3,
    "ideas_in_flight": 2,
    "experiments_running": 2,
    "experiments_concluded": 1,
    "decisions_logged": 4,
    "decisions_pending_review": 3,
    "active_learning_items": 3,
    "opportunities_discovered": 4,
    "opportunities_pursuing": 1,
    "project_health_breakdown": {"green": 2, "yellow": 1, "red": 1},
    "idea_funnel_breakdown": {
      "captured": 0, "explored": 0, "validated": 1,
      "planned": 1, "executing": 1, "completed": 1, "abandoned": 0
    },
    "stagnation_alerts": [
      {
        "type": "project_stagnation",
        "id": "proj-3",
        "title": "Edge-Compute Vision Pipeline",
        "reason": "Project has red health or no recent updates. Progress at 25%."
      }
    ]
  }
  ```

---

## 14. Grounded AI Studio

All AI Studio endpoints strictly enforce the 4-bracket truth taxonomy (`[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, `[AI RECOMMENDATION]`).

### `POST /api/ai/daily-briefing`
- **Purpose:** Synthesizes an executive morning digest from active P0 tasks, approaching deadlines, and blockers.
- **Response (200 OK):** `{"type": "daily_briefing", "content": "# Markdown content..."}`

### `POST /api/ai/weekly-review`
- **Purpose:** Produces an operational retrospective analyzing tasks completed in the past 7 days, idea transitions, and drag factors.
- **Response (200 OK):** `{"type": "weekly_review", "content": "# Markdown content..."}`

### `POST /api/ai/analyze-project/{project_id}`
- **Purpose:** Conducts a deep architectural diagnostic on a specific project, identifying blindspots and missing deadlines.
- **Response (200 OK):** `{"type": "project_analysis", "project_id": "...", "content": "..."}`

### `POST /api/ai/analyze-idea/{idea_id}`
- **Purpose:** Adversarial stress-test for an idea, formulating unvalidated assumptions and designing a falsifiable experiment.
- **Response (200 OK):** `{"type": "idea_analysis", "idea_id": "...", "content": "..."}`

### `POST /api/ai/review-decision/{decision_id}`
- **Purpose:** Retrospective calibration audit evaluating stated expectations against actual outcomes to detect cognitive biases.
- **Response (200 OK):** `{"type": "decision_review", "decision_id": "...", "content": "..."}`

---

## 15. Data Seeding / Reset

### `POST /api/seed`
- **Purpose:** Populates baseline demonstration domain entities into an empty database or resets test states.
- **Response (200 OK):** `{"status": "success", "message": "Demonstration data initialized."}`
