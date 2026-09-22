# Master Documentation Index

This master index catalogs all technical documentation files across the **Personal Command Center** knowledge system. Every file is navigable, indexed, and cross-referenced.

---

## 📑 Core Documentation Portals
- [Documentation Home](README.md) — Portal entry point, reading tracks, and high-level orientation.
- [Documentation Audit & Gap Assessment](DOCUMENTATION-AUDIT.md) — Initial audit, gap classification, and completeness matrix.
- [Documentation Traceability Matrix](documentation-traceability.md) — Source code line citations and verification confidence levels.
- [Documentation Maintenance Policy](documentation-maintenance.md) — PR checklists and ongoing documentation hygiene guidelines.
- [Documentation Changelog](CHANGELOG.md) — Detailed revision history for the documentation department.

---

## 🏛️ System Architecture
- [Architecture Overview](architecture/index.md) — High-level architecture, design philosophy, and core layers.
- [System Architecture](architecture/system-architecture.md) — End-to-end system context, runtime topology, and boundaries.
- [Component Architecture](architecture/component-architecture.md) — Service decomposition (`Repository`, `AIService`, `GraphService`, `SearchService`, `MetricsService`).
- [Data Flow Architecture](architecture/data-flow.md) — Ingestion, persistence, state transitions, and graph edge synthesis.
- [Runtime Flows & Sequences](architecture/runtime-flows.md) — Sequence diagrams for Daily Briefings, Omni-Search, Quick Capture, and Seeding.

---

## 🔌 API Reference
- [API Overview & Standards](api/index.md) — Protocol conventions, status codes, content types, and error handling.
- [Endpoint Reference](api/endpoints.md) — Complete specifications for all 24 REST endpoints with examples.
- [Schema Catalog](api/schemas.md) — Pydantic models, request bodies, response shapes, and validation rules.

---

## 💻 Developer Guides
- [Development Overview](development/index.md) — DX philosophy, toolchain summary, and repo structure.
- [Local Setup & Bootstrapping](development/local-setup.md) — Step-by-step setup with Python 3.14, virtual environments, and dependencies.
- [Development Workflows](development/workflows.md) — Everyday commands, running the server, seeding data, and testing.
- [Engineering Conventions](development/conventions.md) — Code style, type annotations, naming conventions, and file organization.

---

## ⚙️ Configuration Reference
- [System Configuration](configuration/index.md) — Comprehensive guide to environment variables (`COMMAND_CENTER_DB`, `GEMINI_API_KEY`, `PORT`, `HOST`), defaults, types, and security handling.

---

## 🗄️ Database & Storage
- [Database Overview](database/index.md) — SQLite architecture, WAL mode, foreign key enforcement, and connection management.
- [Schema Specification](database/schema.md) — Detailed table definitions, constraints, indexes, and full ER diagram.
- [Queries & Performance](database/queries-and-performance.md) — Index analysis, JSON column querying, and backup/vacuum maintenance.

---

## 🌐 External Integrations
- [Integrations Reference](integrations/index.md) — Google Gemini API integration (`gemini-2.5-flash`), Model Context Protocol (MCP) roadmap, and offline resilience.

---

## 📨 Messaging & Concurrency
- [Messaging & Event Architecture](messaging/index.md) — Synchronous in-process request cycle, transactional SQLite writes, and future async event roadmap.

---

## 🧪 Testing & Verification
- [Testing Strategy & Test Suites](testing/index.md) — Pytest suite execution, test coverage analysis, fixtures, and documentation validation tests.

---

## 🚀 Deployment & Operations
- [Deployment Guide](deployment/index.md) — Standalone Uvicorn hosting, local systemd service unit, and containerization blueprint.
- [Operations Runbook](operations/runbook.md) — Production operations, health probes, backup routines, database recovery, and monitoring.
- [Troubleshooting Matrix](operations/troubleshooting.md) — Diagnostic guide for database locks, missing keys, port collisions, and corrupted state.

---

## 🛡️ Security & Privacy
- [Security Architecture](security/index.md) — Local sovereignty model, CORS configuration, sensitive data protection, and dependency safety.
- [Security Review](security/security-review.md) — Formal security audit, risk assessment, and recommended hardening measures.

---

## 🧠 Domain Knowledge & Reference
- [Business Rules Catalog](business-rules.md) — Formal inventory of domain logic, state machines, grounding tags, and threshold heuristics.
- [Codebase Map](codebase-map.md) — Comprehensive directory and file-level responsibility map.
- [Domain Glossary](glossary.md) — Definitions for 40+ domain terms, acronyms, and technical concepts.
- [Frequently Asked Questions (FAQ)](faq.md) — Multi-perspective Q&A for new developers, senior engineers, DevOps, QA, and architects.
