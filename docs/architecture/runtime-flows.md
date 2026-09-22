# Runtime Execution Flows & Sequences

This document illustrates the primary runtime execution sequences of the **Personal Command Center**.

---

## 1. Application Startup & Initialization Flow

Upon server launch, FastAPI's `@asynccontextmanager lifespan` coordinates database schema verification and seed population:

```mermaid
sequenceDiagram
    autonumber
    participant CLI as Terminal / run.sh
    participant Uvicorn as Uvicorn ASGI Server
    participant App as FastAPI App (main.py)
    participant DB as Database Manager (database.py)
    participant Seed as Seed Module (seed_data.py)
    participant SQLite as SQLite Storage (personal_os.db)

    CLI->>Uvicorn: exec uvicorn app.main:app --host 127.0.0.1 --port 8000
    Uvicorn->>App: Initialize Lifespan Context
    App->>DB: init_db()
    DB->>SQLite: PRAGMA journal_mode = WAL;
    DB->>SQLite: PRAGMA foreign_keys = ON;
    DB->>SQLite: CREATE TABLE IF NOT EXISTS [9 tables]
    DB->>SQLite: CREATE INDEX IF NOT EXISTS [15 indexes]
    DB-->>App: Database initialized
    App->>Seed: seed_database()
    Seed->>SQLite: SELECT COUNT(*) FROM projects
    alt Database Empty (COUNT == 0)
        Seed->>SQLite: Insert 4 Projects, 4 Ideas, 4 Experiments, 4 Decisions, etc.
        Seed-->>App: Baseline demonstration data populated
    else Database Already Seeded (COUNT > 0)
        Seed-->>App: Skipping seed population
    end
    App-->>Uvicorn: Lifespan yield (Ready to receive traffic)
    Uvicorn-->>CLI: Application startup complete. Uvicorn running on http://127.0.0.1:8000
```

---

## 2. Tactical Daily Briefing Runtime Sequence

Triggered either by clicking the "Daily Briefing" HUD button or pressing the keyboard hotkey `B`:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant HUD as Browser HUD (app.js)
    participant API as REST Client (api.js)
    participant Router as FastAPI Router (main.py)
    participant AISvc as AIService (ai_service.py)
    participant Repo as Repository (repository.py)
    participant Gemini as Google Gemini API (Optional)

    User->>HUD: Press 'B' Key / Click Briefing Button
    HUD->>HUD: Show "Synthesizing Grounded Briefing..." spinner
    HUD->>API: API.getDailyBriefing()
    API->>Router: POST /api/ai/daily-briefing
    Router->>AISvc: AIService.generate_daily_briefing()
    
    AISvc->>Repo: Repository.get_tasks()
    AISvc->>Repo: Repository.get_projects(status="active")
    
    AISvc->>AISvc: Filter P0 Critical Tasks, Blockers, Overdue Items
    AISvc->>AISvc: Assemble Factual Grounding Context
    
    alt GEMINI_API_KEY Configured & Network Available
        AISvc->>Gemini: POST generate_content(model="gemini-2.5-flash", prompt, system_instruction)
        Gemini-->>AISvc: Generated Markdown with [FACT], [REC], etc.
    else GEMINI_API_KEY Missing or Network Error
        AISvc->>AISvc: Invoke Deterministic Rule Engine
        AISvc->>AISvc: Format Structured Markdown with Grounding Tags
    end
    
    AISvc-->>Router: String Content
    Router-->>API: JSON { type: "daily_briefing", content: "..." }
    API-->>HUD: Resolve Promise
    HUD->>HUD: Render Markdown in Slide-Over Drawer
    HUD-->>User: Present High-Impact Briefing
```

---

## 3. Idea-to-Experiment Lifecycle Flow

Illustrates how an embryonic thought matures into empirical science:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant HUD as Browser HUD
    participant Router as FastAPI Router
    participant Repo as Repository
    participant DB as SQLite DB

    User->>HUD: Quick Capture Idea ("Adaptive Speculative Decoding")
    HUD->>Router: POST /api/ideas (status="captured")
    Router->>Repo: create_idea()
    Repo->>DB: INSERT INTO ideas ...
    DB-->>HUD: Idea Created (ID: idea-1)

    Note over User,DB: Stage 1: Exploration & Stress-Testing
    User->>HUD: Trigger AI Stress-Test on idea-1
    HUD->>Router: POST /api/ai/analyze-idea/idea-1
    Router-->>HUD: Returns Assumptions & Recommended Test Design

    Note over User,DB: Stage 2: Idea Validation Transition
    User->>HUD: Click "Advance Stage" ➔ Validated
    HUD->>Router: POST /api/ideas/idea-1/transition?target_status=validated
    Router->>Repo: update_idea()
    Repo->>DB: UPDATE ideas SET status='validated' WHERE id='idea-1'

    Note over User,DB: Stage 3: Launch Empirical Experiment
    User->>HUD: Register Experiment linking idea_id='idea-1'
    HUD->>Router: POST /api/experiments { idea_id: "idea-1", hypothesis: "...", design: "..." }
    Router->>Repo: create_experiment()
    Repo->>DB: INSERT INTO experiments ...

    Note over User,DB: Stage 4: Conclude Experiment with Evidence
    User->>HUD: Log Actual Result & Conclusion
    HUD->>Router: PUT /api/experiments/exp-1 { status: "concluded", evidence: "...", actual_result: "..." }
    Router->>Repo: update_experiment()
    Repo->>DB: UPDATE experiments ...
    
    Note over User,DB: Knowledge Graph automatically surfaces edge: idea-1 --validates--> exp-1
```
