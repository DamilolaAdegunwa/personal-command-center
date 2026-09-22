# Data Flow Architecture Specification

This document details the data lifecycle, transformation pipelines, and data flow architectures within the **Personal Command Center**.

---

## 1. Entity Mutation & Persistence Pipeline

Every state change across the 9 primary domain entities follows a strict unidirectional pipeline ensuring schema validation, relational consistency, and immediate durability:

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Client
    participant Frontend as HUD UI (app.js / api.js)
    participant Router as FastAPI Router (app.main)
    participant Schema as Pydantic Schema (app.models)
    participant Repo as Repository (app.repository)
    participant DB as SQLite DB (personal_os.db)

    User->>Frontend: Fill Form / Trigger Action (e.g., Create Idea)
    Frontend->>Router: POST /api/ideas { title, category, description, ... }
    Router->>Schema: Validate Payload (IdeaCreate)
    alt Validation Failure
        Schema-->>Router: ValidationError (422 Unprocessable Entity)
        Router-->>Frontend: JSON Error Response
        Frontend-->>User: Display Toast Error Alert
    else Validation Success
        Router->>Repo: Repository.create_idea(data)
        Repo->>Repo: Generate UUIDv4 & UTC ISO-8601 Timestamps
        Repo->>DB: INSERT INTO ideas VALUES (...)
        DB-->>Repo: Row Committed to WAL Journal
        Repo->>DB: SELECT * FROM ideas WHERE id = ?
        DB-->>Repo: Freshly Persisted Record
        Repo-->>Router: Idea Pydantic Instance
        Router-->>Frontend: HTTP 200 OK + JSON Payload
        Frontend-->>User: Render Idea Card & Play Glow Animation
    end
```

---

## 2. Knowledge Graph Aggregation Pipeline

The Knowledge Graph combines implicit relational links derived from foreign keys with explicit user-defined relationships into a unified graph topology:

```mermaid
flowchart TD
    subgraph Storage ["SQLite Storage"]
        T_Proj[("projects")]
        T_Idea[("ideas")]
        T_Exp[("experiments")]
        T_Dec[("decisions")]
        T_Res[("research_entries")]
        T_Learn[("learning_items")]
        T_Opp[("opportunities")]
        T_Edge[("knowledge_edges")]
    end

    subgraph Service ["app.graph_service.GraphService"]
        Fetch["1. Fetch All Domain Records"]
        NodeBuild["2. Construct GraphNodes (id, label, type, subtitle, status, health)"]
        ImplicitEdges["3. Resolve Implicit Foreign Key Edges:
        - Idea ➔ Project (spawns)
        - Idea ➔ Experiment (validates)
        - Experiment ➔ Project (informs)
        - Research ➔ Project (informs)"]
        ExplicitEdges["4. Ingest Explicit Edges from knowledge_edges"]
        Dedupe["5. Deduplicate Node IDs & Bidirectional Edge Keys"]
        Package["6. Assemble GraphData (nodes, edges)"]
    end

    subgraph Client ["Client SVG Renderer (graph.js)"]
        Layout["Force Simulation Coordinate Calculation"]
        DOMRender["Render SVG Nodes, Badges & Curved SVG Edges"]
    end

    T_Proj & T_Idea & T_Exp & T_Dec & T_Res & T_Learn & T_Opp & T_Edge --> Fetch
    Fetch --> NodeBuild
    NodeBuild --> ImplicitEdges
    ImplicitEdges --> ExplicitEdges
    ExplicitEdges --> Dedupe
    Dedupe --> Package
    Package -->|HTTP GET /api/graph| Layout
    Layout --> DOMRender
```

---

## 3. Universal Omni-Search Data Flow

The search pipeline evaluates text queries across all 8 domain entity collections using an in-memory token scoring algorithm:

```mermaid
flowchart TD
    Query["Search Request: GET /api/search?q=attention&types=research,idea"]
    Tokenize["1. Tokenize query string into lowercase tokens ['attention']"]
    
    subgraph EntityEvaluation ["2. Multi-Collection Evaluation"]
        direction TB
        E1["Scan Research Entries (research_question, topic, investigations, conclusions)"]
        E2["Scan Ideas (title, description, origin, next_action)"]
        E3["Scan Tasks (title, blocker_reason, tags)"]
        E4["Scan Projects, Experiments, Decisions, Learning, Opportunities..."]
    end

    ScoreCalc["3. Relevance Scoring Function:
    - Token in Title: +5.0 points
    - Token in Content/Snippet: +1.5 points
    - Project Entity Boost: +1.0 point"]

    Filter["4. Filter by optional query parameters:
    - status
    - priority
    - tag"]

    SortLimit["5. Sort descending by relevance_score & slice [:limit] (Default 40 items)"]
    ReturnResults["6. Return List[SearchResultItem]"]

    Query --> Tokenize
    Tokenize --> EntityEvaluation
    EntityEvaluation --> ScoreCalc
    ScoreCalc --> Filter
    Filter --> SortLimit
    SortLimit --> ReturnResults
```

---

## 4. Grounded AI Intelligence Pipeline

The AI pipeline guarantees truth preservation by separating verified repository data from generative recommendations:

```mermaid
flowchart TB
    Trigger["Client Request: POST /api/ai/daily-briefing"]
    
    subgraph Extraction ["1. Ground Truth Extraction"]
        DBTasks["Extract Tasks (P0, P1, Blocked, Overdue)"]
        DBProj["Extract Active Projects & Health"]
        DBDeadlines["Calculate Deadlines (Next 72 Hours)"]
    end

    subgraph PromptConstruct ["2. Context Construction & System Tagging Rules"]
        Context["Assemble factual summary string:
        - Date: 2026-09-22
        - Projects: Nexus (Green, 78%), Edge Vision (Red, 25%)
        - P0 Tasks: [...]
        - Blocked: [...]"]
        Rule["System Prompt enforces 4-bracket taxonomy:
        [FACT], [USER CONTEXT], [ASSUMPTION], [AI RECOMMENDATION]"]
    end

    subgraph ExecutionBranch ["3. Execution Engine Selection"]
        KeyCheck{"GEMINI_API_KEY Available?"}
        LLM["Google Gemini Client (gemini-2.5-flash):
        generate_content(prompt, system_instruction)"]
        Heuristic["Deterministic Rule Engine:
        Evaluates task states, deadlines, and project health locally.
        Applies pre-defined tactical heuristics."]
    end

    Response["Return Markdown Response to Client"]

    Trigger --> Extraction
    DBTasks & DBProj & DBDeadlines --> Context
    Context --> Rule
    Rule --> KeyCheck
    KeyCheck -- Yes --> LLM
    KeyCheck -- No (or network error) --> Heuristic
    LLM --> Response
    Heuristic --> Response
```
