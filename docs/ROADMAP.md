# Personal Command Center: Evolutionary Roadmap

## Phase 1: Foundation & Core Tactical HUD (Delivered in v1.0.0)
- [x] Complete domain modeling for Tasks, Projects, Ideas, Experiments, Decisions, Research, Learning, and Opportunities.
- [x] High-density tactical HUD interface with dark aesthetic, status indicators, and keyboard shortcuts (`Cmd+K`, `C`, `B`).
- [x] Interactive visual SVG Personal Knowledge Graph.
- [x] Universal Omni-Search with instant multi-entity faceted filtering.
- [x] Grounded AI Intelligence Studio (Daily Briefing, Weekly Review, Project Diagnostic, Idea Evaluation, Decision Audit).
- [x] Situational awareness metrics and stagnation detection (>14 days inactive).
- [x] Full SQLite persistence with seed data and comprehensive automated test suite.

---

## Phase 2: Autonomous Intelligence & Context Ingestion (v1.1 - v1.2)
- [ ] **Model Context Protocol (MCP) Server**: Expose Personal Command Center tools and resources via MCP so Antigravity or Claude agents can autonomously read tasks and register research findings.
- [ ] **Git Repository Activity Watcher**: Automatically scan local git repos in `/Users/dammy/Documents/GitHub` to increment project progress and log commits as task updates.
- [ ] **Calendar & Email Sentinel**: Ingest meeting obligations and extract external commitments directly into the Today cockpit.

---

## Phase 3: Cognitive Amplification & Neural Memory (v2.0)
- [ ] **Local Vector Search (`sqlite-vec`)**: Hybrid lexical and dense vector search across technical notes and paper abstracts.
- [ ] **Proactive Stagnation Alerts**: Background cron job pushing macOS notification center alerts when a P0 project is blocked for >48 hours.
- [ ] **Voice-Activated Tactical Briefing**: Local text-to-speech audio playback of the morning briefing.
