# 📚 Personal Command Center Documentation Portal

Welcome to the central technical documentation portal for the **Personal Command Center (Personal OS)**. This documentation system is authored, verified, and maintained to provide an authoritative, transparent, and navigable knowledge base for developers, architects, operators, and security engineers.

---

## 1. System Overview

The **Personal Command Center** is a high-performance, local-first personal operating system designed for an individual living and working in the AI era. It resolves cognitive fragmentation by anchoring scattered ideas, tasks, research papers, decisions, and experiments into an interconnected relational knowledge graph.

### Core Architectural Pillars
- **Local Sovereignty & Persistence**: Built on Python 3.14+, FastAPI, and an embedded SQLite transactional database running in Write-Ahead Logging (`WAL`) mode with foreign key enforcement. All data remains strictly on the user's local disk.
- **Cognitive Grounding**: The built-in AI intelligence studio enforces strict truth boundaries. Every insight is tagged with `[FACT]`, `[USER CONTEXT]`, `[ASSUMPTION]`, or `[AI RECOMMENDATION]`, eliminating generative hallucinations.
- **Relational Traceability**: Connects ideas to falsifiable experiments, empirical conclusions to strategic decisions, and decisions to concrete execution projects.
- **Keyboard-Driven Cockpit**: Single-Page HUD interface featuring instant universal omni-search (`Cmd+K`), quick capture (`C`), daily briefing generation (`B`), and an interactive force-directed SVG knowledge graph.

---

## 2. Documentation Directory Map

```
docs/
├── README.md                          # Documentation Portal Gateway (You are here)
├── index.md                           # Master Hierarchical Index & Deep Links
├── DOCUMENTATION-AUDIT.md             # Gap Assessment & Completeness Matrix
├── business-rules.md                  # Catalog of Business Logic & State Machines
├── codebase-map.md                    # Structural Architecture & Module Guide
├── glossary.md                        # Formal Technical & Domain Terminology
├── faq.md                             # Role-Based Frequently Asked Questions
├── documentation-traceability.md      # Claim-to-Code Source Verification Matrix
├── documentation-maintenance.md       # Change Management & PR Checklists
├── CHANGELOG.md                       # Comprehensive Documentation History
├── architecture/                      # Architectural Blueprints & Diagrams
│   ├── index.md                       # Architecture Overview & Design Principles
│   ├── system-architecture.md         # Full System Architecture & Boundaries
│   ├── component-architecture.md      # Service Decomposition & Modular Design
│   ├── data-flow.md                   # Data Ingestion, Storage & Graph Pipelines
│   └── runtime-flows.md               # Synchronous & Asynchronous Sequence Flows
├── api/                               # Complete REST API Specifications
│   ├── index.md                       # API Standards, Conventions & Auth Notes
│   ├── endpoints.md                   # Exhaustive Documentation of all 24 Endpoints
│   └── schemas.md                     # Pydantic v2 Request & Response Schemas
├── development/                       # Engineering Guides & Local Setup
│   ├── index.md                       # Developer Experience Overview
│   ├── local-setup.md                 # Prerequisites, Environment & Bootstrapping
│   ├── workflows.md                   # Common Workflows, Seed Data & Debugging
│   └── conventions.md                 # Code Organization, Typing & Style Rules
├── configuration/                     # System Settings & Parameter Catalog
│   └── index.md                       # Environment Variables, Defaults & Sensitivity
├── database/                          # SQLite Schema & Performance Engineering
│   ├── index.md                       # Database Technology & Connection Manager
│   ├── schema.md                      # Tables, Indexes, Constraints & ER Diagram
│   └── queries-and-performance.md     # Index Utilization, WAL Mode & Queries
├── integrations/                      # External Services & Protocol Bridges
│   └── index.md                       # Google Gemini API, MCP Roadmap & Citations
├── messaging/                         # Event Handling & Concurrency Semantics
│   └── index.md                       # Synchronous Execution & Async Roadmap
├── testing/                           # Quality Assurance & Verification
│   └── index.md                       # Test Strategy, Pytest Suites & Coverage Gaps
├── deployment/                        # Runtime Deployment & Containerization
│   └── index.md                       # Standalone Process, Uvicorn, Systemd & Docker
├── operations/                        # Production Operations & Support
│   ├── runbook.md                     # Health Probes, Backups & Maintenance
│   └── troubleshooting.md             # Symptom-Cause-Diagnostic-Resolution Matrix
└── security/                          # Security Assessment & Threat Model
    ├── index.md                       # Security Controls, Storage & Network Policy
    └── security-review.md             # Formal Security Audit & Recommendations
```

---

## 3. Reading Paths by Role

Select the documentation track most relevant to your objective:

### 🚀 For New Developers
1. Start with [docs/development/local-setup.md](development/local-setup.md) to bootstrap your Python 3.14 virtual environment.
2. Review the repository organization in [docs/codebase-map.md](codebase-map.md).
3. Follow the common development cycles in [docs/development/workflows.md](development/workflows.md).
4. Review the core domain concepts in [docs/glossary.md](glossary.md).

### 🏛️ For Software Architects
1. Review the overarching topology in [docs/architecture/system-architecture.md](architecture/system-architecture.md).
2. Examine service decomposition in [docs/architecture/component-architecture.md](architecture/component-architecture.md).
3. Inspect runtime execution flows and sequence diagrams in [docs/architecture/runtime-flows.md](architecture/runtime-flows.md).
4. Review the business state machines in [docs/business-rules.md](business-rules.md).

### 🔌 For API Consumers & Frontend Engineers
1. Read the API standards and overview in [docs/api/index.md](api/index.md).
2. Browse the complete endpoint reference in [docs/api/endpoints.md](api/endpoints.md).
3. Review Pydantic data schemas in [docs/api/schemas.md](api/schemas.md).

### 🛠️ For Operations & Support Engineers
1. Read the production operations procedures in [docs/operations/runbook.md](operations/runbook.md).
2. Use the symptom-to-resolution guide in [docs/operations/troubleshooting.md](operations/troubleshooting.md).
3. Inspect configuration parameters in [docs/configuration/index.md](configuration/index.md).
4. Review backup and restore workflows in [docs/database/queries-and-performance.md](database/queries-and-performance.md).

### 🔒 For Security & Compliance Engineers
1. Review the security posture and threat model in [docs/security/index.md](security/index.md).
2. Inspect the structured security assessment in [docs/security/security-review.md](security/security-review.md).

---

## 4. Known Limitations & Human Confirmation Flags

As established from repository evidence:
1. **Single-User / Local-Only Authentication**: The application currently has no authentication or session isolation. It is engineered strictly as a local personal operating system running on `127.0.0.1`.
2. **Synchronous In-Process AI Invocations**: AI generation endpoints (`/api/ai/*`) execute synchronously within the FastAPI request cycle. External Gemini API calls introduce latency (1-3 seconds); when unconfigured, the fallback deterministic rule engine responds in <5ms.
3. **No External Message Broker**: There is no Kafka, RabbitMQ, or Redis broker present in the codebase. All state operations execute directly against SQLite.
4. **Requires Human Confirmation**: Integration with external calendar feeds and automated git commit ingestion is documented as an upcoming roadmap phase (`v1.1+`) and is not currently functional in the `v1.0.0` codebase.

---

## 5. Automated Documentation Verification

To ensure documentation remains accurate and free of dead links or drifted endpoints, run the documentation validation suite:

```bash
# Validate internal links and endpoint parity
python3 scripts/validate_docs.py

# Run test suite including documentation validation
PYTHONPATH=. pytest -v tests/
```
