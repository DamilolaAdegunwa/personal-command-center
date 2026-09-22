# Domain Glossary & Technical Terminology

This glossary defines technical terms, domain concepts, architectural patterns, and abbreviations used throughout the **Personal Command Center**.

---

## A
- **ACID (Atomicity, Consistency, Isolation, Durability):** Standard database transaction properties guaranteed by SQLite in WAL mode.
- **ASGI (Asynchronous Server Gateway Interface):** The modern Python specification for asynchronous web servers, implemented by Uvicorn.
- **Assumption Tag (`[ASSUMPTION]`):** An AI grounding marker denoting inferred risks, unverified hypotheses, or missing temporal boundaries.

## C
- **Cognitive Grounding:** The architectural practice of anchoring every generative AI statement to verified, verifiable database facts to eliminate hallucinations.
- **Completed At:** An ISO-8601 UTC timestamp automatically applied to a task record when its status transitions to `completed`.

## D
- **Decision Amnesia:** The cognitive failure where high-stakes technical decisions are forgotten, preventing teams or individuals from retrospectively auditing whether their judgment was calibrated.
- **Decision Intelligence Log:** A structured database module for capturing context, alternatives, assumptions, evidence, and expected vs. actual outcomes.
- **Deep Work:** An energy-level classification for tasks demanding intense, uninterrupted cognitive focus.

## E
- **Energy Level:** A metadata classification (`deep_work`, `quick_win`, `administrative`) assigned to tasks to help builders align work with cognitive capacity.
- **Empirical Experiment:** A structured scientific test designed to falsify or validate an idea hypothesis (`Hypothesis ➔ Design ➔ Evidence ➔ Conclusion`).

## F
- **Fact Tag (`[FACT]`):** An AI grounding marker indicating a statement extracted directly from verified database records without interpretation.
- **Force Simulation:** An algorithm used in `static/js/graph.js` to dynamically position knowledge graph nodes based on physics-inspired attraction and repulsion forces.

## G
- **Gemini (Google GenAI):** Google's multimodal foundation model platform (`gemini-2.5-flash`), optionally integrated for strategic intelligence synthesis.
- **Grounded AI Studio:** The application subsystem responsible for producing daily briefings, project diagnostics, idea stress-tests, and decision audits.

## H
- **HUD (Heads-Up Display):** The tactical, high-density dark UI design pattern employed by the frontend interface.

## I
- **Idea Lifecycle Pipeline:** A 7-stage state machine (`captured` ➔ `explored` ➔ `validated` ➔ `planned` ➔ `executing` ➔ `completed` / `abandoned`) guiding concepts from spark to completion.
- **Implicit Edge:** A relational knowledge graph connection derived dynamically from database foreign keys (e.g. `Idea ➔ Project`).

## K
- **Knowledge Edge:** A directed, typed connection (`leads_to`, `validates`, `informs`, `implements`, `spawns`, `depends_on`, `references`) linking two domain entities.
- **Knowledge Graph:** The interconnected network of ideas, projects, experiments, decisions, and research visualizing organizational memory.

## L
- **Lifespan Manager:** FastAPI's modern startup and shutdown protocol (`@asynccontextmanager lifespan`) used to initialize database tables and seed data.
- **Local Sovereignty:** The design principle ensuring all personal data, memory, and code remain on the user's local machine without cloud lock-in.

## O
- **Omni-Search:** The universal, multi-entity search palette accessible via `Cmd+K` that scores and indexes records across all 8 domain collections.
- **Opportunity Radar:** A strategic module tracking emerging technology, business, career, or grant opportunities.

## P
- **P0 Critical:** The highest task priority tier, designating urgent fire drills requiring immediate deep-work intervention.
- **Personal OS:** A personal operating system designed to manage knowledge, commitments, experiments, and strategic direction for a technical builder.
- **Project Health:** A categorical status (`green`, `yellow`, `red`) representing project momentum and risk posture.

## Q
- **Quick Capture:** A lightweight global modal triggered via the `C` key that enables instant capture of tasks, ideas, decisions, or research.

## R
- **Recommendation Tag (`[AI RECOMMENDATION]`):** An AI grounding marker indicating an actionable proposal synthesized by algorithmic logic.
- **Research Dossier:** A structured investigation record capturing research questions, findings, citations, and unresolved questions.

## S
- **Stagnation Alert:** An automated warning emitted when an active project has red health or no updates in >14 days, or when a task is blocked.

## U
- **User Context Tag (`[USER CONTEXT]`):** An AI grounding marker indicating explicit intentions, notes, or descriptions recorded by the user.

## W
- **WAL Mode (Write-Ahead Logging):** An SQLite journaling mode where writes are appended sequentially to a separate log file, allowing concurrent readers without lock contention.
