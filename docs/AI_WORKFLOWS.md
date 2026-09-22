# AI Intelligence Workflows & Grounding Architecture

## 1. Zero-Hallucination Grounding Taxonomy

A primary pitfall of AI productivity software is the silent invention of deadlines, commitments, or progress. In the Personal Command Center, every AI response is strictly anchored in the user's database records using four transparent markers:

| Bracket Tag | Semantics | Data Source |
|---|---|---|
| `[FACT]` | Verifiable reality extracted directly from records | Tasks, timestamps, status values, blockers |
| `[USER CONTEXT]` | Explicit desires, notes, and rationales recorded by the user | Description fields, decision context, journals |
| `[ASSUMPTION]` | Inferences or risks identified from missing or stale data | Gaps, expired deadlines, missing test designs |
| `[AI RECOMMENDATION]` | Actionable proposal for tactical maneuver or prioritization | Algorithmic synthesis / LLM strategic analysis |

---

## 2. The 5 Core Intelligence Workflows

### 2.1 Tactical Daily Briefing (`/api/ai/daily-briefing`)
- **Objective:** Give the user an unvarnished 60-second operational snapshot upon boot.
- **Inputs:** Active P0/P1 tasks, deadlines within 72 hours, blocked items, stale projects (>14d inactive).
- **Format:**
  - `## Executive Summary`
  - `## Immediate Fire Drills (P0 & Blocked)`
  - `## Critical Deadlines (Next 72 Hours)`
  - `## Recommended Tactical Sequence (1-2-3)`

### 2.2 Strategic Weekly Review (`/api/ai/weekly-review`)
- **Objective:** Retrospective analysis of the preceding 7 days to calibrate velocity and focus.
- **Inputs:** Tasks completed in past 7 days, ideas moved through stages, experiments concluded, decisions reviewed, stalled projects.
- **Format:**
  - `## Accomplishments & Closed Loops`
  - `## Stalled Initiatives & Friction Points`
  - `## Emerging Opportunities & Idea Transitions`
  - `## Focus Realignment for Next Sprint`

### 2.3 Project Deep Diagnostic (`/api/ai/analyze-project/{id}`)
- **Objective:** Perform a rigorous architecture/management audit on a single project.
- **Inputs:** Project details, connected tasks, linked experiments, research dossiers, health rating.
- **Format:**
  - `## Health & Trajectory Assessment`
  - `## Missing Information & Blindspots`
  - `## Dependency & Blocker Analysis`
  - `## High-Impact Next Actions`

### 2.4 Idea Evaluation Engine (`/api/ai/analyze-idea/{id}`)
- **Objective:** Subject a raw idea to rigorous stress-testing before building.
- **Inputs:** Idea title, description, category, related research, experiment links.
- **Format:**
  - `## Problem Sharpness & Value Proposition`
  - `## Critical Hidden Assumptions`
  - `## Counter-Arguments & Failure Modes`
  - `## Empirical Experiment Blueprint (Hypothesis -> Test)`

### 2.5 Decision Retrospective Audit (`/api/ai/review-decision/{id}`)
- **Objective:** Review past decisions against recorded outcomes to eliminate cognitive bias.
- **Inputs:** Decision context, alternatives considered, assumptions, confidence level, expected outcome, actual outcome.
- **Format:**
  - `## Expectation vs. Reality Comparison`
  - `## Confidence Calibration Score`
  - `## Overlooked Variables in Retrospect`
  - `## Meta-Principles & Heuristics Extracted`

---

## 3. Fallback & Offline Resilience
The system operates seamlessly whether an external LLM API key is present or not. When `GEMINI_API_KEY` is not detected, an intelligent local rule-based heuristic engine evaluates timestamps, health metrics, and graph connections to produce high-value, structured intelligence reports without external dependencies.
