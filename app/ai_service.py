import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from app.repository import Repository
from app.models import Task, Project, Idea, Experiment, Decision, ResearchEntry, LearningItem, Opportunity

# Check for Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIService:
    @staticmethod
    def _call_gemini_if_available(prompt: str, system_instruction: str) -> Optional[str]:
        if not GEMINI_API_KEY:
            return None
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"system_instruction": system_instruction}
            )
            if response and response.text:
                return response.text
        except Exception:
            return None
        return None

    # --- 1. DAILY BRIEFING ---
    @staticmethod
    def generate_daily_briefing() -> str:
        now = datetime.now(timezone.utc)
        today_str = now.strftime("%Y-%m-%d")
        
        # Ground Truth Extraction
        tasks = Repository.get_tasks()
        projects = Repository.get_projects(status="active")
        
        p0_tasks = [t for t in tasks if t.priority.value == "p0_critical" and t.status.value != "completed"]
        p1_tasks = [t for t in tasks if t.priority.value == "p1_high" and t.status.value != "completed"]
        blocked_tasks = [t for t in tasks if t.status.value == "blocked"]
        
        overdue_tasks = []
        upcoming_deadlines = []
        for t in tasks:
            if t.status.value != "completed" and t.deadline:
                try:
                    dl_dt = datetime.fromisoformat(t.deadline if "T" in t.deadline else t.deadline + "T23:59:59+00:00")
                    diff_days = (dl_dt - now).total_seconds() / 86400
                    if diff_days < 0:
                        overdue_tasks.append((t, abs(diff_days)))
                    elif diff_days <= 3.0:
                        upcoming_deadlines.append((t, diff_days))
                except Exception:
                    pass

        # LLM Synthesis Prompt
        system_instruction = (
            "You are the Chief of Staff for a high-velocity AI engineer's Personal Command Center. "
            "You must maintain strict grounding. Every statement MUST use one of these four tags: "
            "[FACT], [USER CONTEXT], [ASSUMPTION], [AI RECOMMENDATION]. "
            "Never fabricate deadlines, tasks, or numbers not given in the data."
        )

        user_prompt = f"""
Current Date: {today_str}
Active Projects Count: {len(projects)}
Projects: {[f"{p.title} (Health: {p.health.value}, Progress: {p.progress_pct}%)" for p in projects[:5]]}
Critical P0 Tasks: {[t.title for t in p0_tasks]}
Blocked Tasks: {[f"{t.title} (Blocker: {t.blocker_reason})" for t in blocked_tasks]}
Overdue Tasks: {[f"{t.title} ({days:.1f} days overdue)" for t, days in overdue_tasks]}
Upcoming Deadlines: {[f"{t.title} in {days:.1f} days" for t, days in upcoming_deadlines]}

Generate a concise, high-impact Daily Briefing covering:
1. Executive Situation Snapshot
2. Immediate Fire Drills (P0 & Blocked)
3. Approaching Deadlines
4. Recommended 3-Step Execution Sequence for Today
"""
        llm_result = AIService._call_gemini_if_available(user_prompt, system_instruction)
        if llm_result:
            return llm_result

        # Heuristic Deterministic Generator
        briefing = []
        briefing.append(f"# 🛰️ Tactical Daily Briefing — {today_str}\n")
        briefing.append("### 1. Executive Situation Snapshot")
        briefing.append(f"- `[FACT]` You have **{len(projects)} active projects**, **{len(p0_tasks)} critical P0 tasks**, and **{len(blocked_tasks)} blocked items** requiring intervention.")
        briefing.append(f"- `[FACT]` Total overdue commitments: **{len(overdue_tasks)}**; deadlines within 72 hours: **{len(upcoming_deadlines)}**.")
        if any(p.health.value == "red" for p in projects):
            red_projects = [p.title for p in projects if p.health.value == "red"]
            briefing.append(f"- `[FACT]` Attention needed: Project(s) flagged RED health: **{', '.join(red_projects)}**.")
        
        briefing.append("\n### 2. Immediate Fire Drills (P0 & Blocked)")
        if p0_tasks or blocked_tasks:
            for t in p0_tasks:
                briefing.append(f"- `[FACT]` **P0 CRITICAL**: {t.title} (Energy: {t.energy_level.value})")
            for b in blocked_tasks:
                briefing.append(f"- `[FACT]` **BLOCKED**: {b.title}")
                briefing.append(f"  - `[USER CONTEXT]` Reason: {b.blocker_reason or 'No blocker reason specified'}")
                briefing.append(f"  - `[AI RECOMMENDATION]` Triage this dependency immediately to prevent cascading sprint delay.")
        else:
            briefing.append("- `[FACT]` No active P0 tasks or blocked items recorded.")

        briefing.append("\n### 3. Approaching Deadlines (Next 72 Hours)")
        if upcoming_deadlines:
            for t, days in upcoming_deadlines:
                briefing.append(f"- `[FACT]` **{t.title}** due in {days*24:.0f} hours (Deadline: {t.deadline})")
        else:
            briefing.append("- `[FACT]` No critical external deadlines within the immediate 72-hour window.")

        briefing.append("\n### 4. Recommended Execution Sequence")
        step = 1
        if blocked_tasks:
            briefing.append(f"{step}. `[AI RECOMMENDATION]` **Resolve Blocker**: Reach out or execute mitigation for `{blocked_tasks[0].title}`.")
            step += 1
        if p0_tasks:
            briefing.append(f"{step}. `[AI RECOMMENDATION]` **Deep Work Block**: Dedicate uninterrupted morning cycle to `{p0_tasks[0].title}`.")
            step += 1
        if upcoming_deadlines:
            briefing.append(f"{step}. `[AI RECOMMENDATION]` **Deadline Prep**: Advance `{upcoming_deadlines[0][0].title}` to avoid last-minute rush.")
            step += 1
        if step <= 3 and projects:
            active_p = projects[0]
            action = active_p.next_actions[0] if active_p.next_actions else "Audit milestones"
            briefing.append(f"{step}. `[AI RECOMMENDATION]` **Strategic Momentum**: Advance `{active_p.title}` next action: '{action}'.")

        briefing.append(f"\n> `[ASSUMPTION]` Generated via deterministic grounded situational engine based on local SQLite state at {now.strftime('%H:%M UTC')}.")
        return "\n".join(briefing)

    # --- 2. WEEKLY REVIEW ---
    @staticmethod
    def generate_weekly_review() -> str:
        now = datetime.now(timezone.utc)
        one_week_ago = now - timedelta(days=7)
        
        tasks = Repository.get_tasks()
        completed_tasks = [t for t in tasks if t.status.value == "completed"]
        recent_completed = []
        for t in completed_tasks:
            if t.completed_at:
                try:
                    c_dt = datetime.fromisoformat(t.completed_at)
                    if c_dt >= one_week_ago:
                        recent_completed.append(t)
                except Exception:
                    pass
        
        projects = Repository.get_projects()
        ideas = Repository.get_ideas()
        opps = Repository.get_opportunities()
        decisions = Repository.get_decisions()
        learning = Repository.get_learning_items()

        system_instruction = (
            "You are a Senior Strategic Coach conducting an operational weekly review. "
            "Strictly distinguish [FACT], [USER CONTEXT], [ASSUMPTION], and [AI RECOMMENDATION]."
        )
        user_prompt = f"""
Recently Completed Tasks (past 7 days): {[t.title for t in recent_completed]}
Active Projects: {[p.title for p in projects if p.status.value == 'active']}
Ideas in Flight: {[i.title for i in ideas if i.status.value in ('validated', 'planned', 'executing')]}
New Opportunities: {[o.title for o in opps if o.status.value == 'evaluating']}
Decisions Logged: {[d.title for d in decisions]}
Active Learning: {[f"{l.title} ({l.progress_pct}%)" for l in learning if l.status.value == 'active']}

Synthesize:
1. Key Accomplishments & Closed Loops
2. Unfinished Commitments & Drag Factors
3. Emerging Opportunities & Idea Evolution
4. High-Priority Directives for the Upcoming Week
"""
        llm_result = AIService._call_gemini_if_available(user_prompt, system_instruction)
        if llm_result:
            return llm_result

        review = []
        review.append("# 📊 Grounded Weekly Operational Retrospective\n")
        review.append("### 1. Key Accomplishments & Closed Loops")
        review.append(f"- `[FACT]` Closed **{len(recent_completed)} tasks** in the past 7-day period.")
        for t in recent_completed[:5]:
            review.append(f"  - `[FACT]` Completed: {t.title}")

        review.append("\n### 2. Unfinished Commitments & Drag Factors")
        blocked = [t for t in tasks if t.status.value == "blocked"]
        review.append(f"- `[FACT]` Currently carrying **{len(blocked)} blocked tasks** across active projects.")
        for b in blocked[:3]:
            review.append(f"  - `[FACT]` Stalled item: {b.title} (Reason: {b.blocker_reason})")
            review.append(f"    - `[AI RECOMMENDATION]` Re-evaluate whether this dependency can be bypassed or descoped.")

        review.append("\n### 3. Ideas, Experiments & Decisions Logged")
        review.append(f"- `[FACT]` Total ideas captured: **{len(ideas)}**; **{len([i for i in ideas if i.status.value == 'validated'])}** validated.")
        review.append(f"- `[FACT]` Decisions logged in system: **{len(decisions)}**.")

        review.append("\n### 4. Learning & Upskilling Velocity")
        for l in learning:
            review.append(f"- `[FACT]` {l.subject}: **{l.title}** ({l.progress_pct}% complete)")
            if l.progress_pct >= 80:
                review.append(f"  - `[AI RECOMMENDATION]` Near milestone! Schedule final practical exercises to solidify retention.")

        review.append(f"\n> `[ASSUMPTION]` Review synthesized from historical audit logs. No data hallucinated.")
        return "\n".join(review)

    # --- 3. PROJECT ANALYSIS ---
    @staticmethod
    def analyze_project(project_id: str) -> str:
        project = Repository.get_project(project_id)
        if not project:
            return f"Project with ID '{project_id}' not found."

        tasks = Repository.get_tasks(project_id=project_id)
        edges = Repository.get_edges("project", project_id)
        experiments = [e for e in Repository.get_experiments() if e.project_id == project_id]
        research = [r for r in Repository.get_research_entries() if r.related_project_id == project_id]

        system_instruction = (
            "You are a Principal Systems Architect and Technical Program Manager. "
            "Provide a rigorous project audit strictly tagging with [FACT], [USER CONTEXT], [ASSUMPTION], [AI RECOMMENDATION]."
        )
        user_prompt = f"""
Project Title: {project.title}
Category: {project.category.value}
Status: {project.status.value}
Health: {project.health.value}
Progress: {project.progress_pct}%
Target Date: {project.target_date}
Description: {project.description}
Next Actions: {project.next_actions}
Tasks Attached: {[f"{t.title} ({t.status.value}, {t.priority.value})" for t in tasks]}
Linked Experiments: {[e.title for e in experiments]}
Linked Research: {[r.research_question for r in research]}

Analyze:
1. Trajectory and Health Verification
2. Missing Information and Blindspots
3. Dependency & Risk Assessment
4. Recommended Tactical Actions
"""
        llm_result = AIService._call_gemini_if_available(user_prompt, system_instruction)
        if llm_result:
            return llm_result

        out = []
        out.append(f"# 🔍 Project Diagnostic: {project.title}\n")
        out.append("### 1. Trajectory & Health Verification")
        out.append(f"- `[FACT]` Status: **{project.status.value.upper()}** | Health: **{project.health.value.upper()}** | Progress: **{project.progress_pct}%**")
        out.append(f"- `[USER CONTEXT]` Description: {project.description or 'No description provided'}")
        out.append(f"- `[FACT]` Associated Tasks: **{len(tasks)}** ({len([t for t in tasks if t.status.value == 'completed'])} completed, {len([t for t in tasks if t.status.value == 'blocked'])} blocked).")

        out.append("\n### 2. Missing Information & Structural Gaps")
        if not project.target_date:
            out.append("- `[ASSUMPTION]` **No explicit target delivery date is recorded**. Without a temporal deadline, project is prone to scope creep.")
            out.append("  - `[AI RECOMMENDATION]` Define target milestone date.")
        if not project.next_actions:
            out.append("- `[FACT]` **Next actions list is empty**.")
            out.append("  - `[AI RECOMMENDATION]` Break down next 3 actionable units of work.")
        if not experiments and not research:
            out.append("- `[FACT]` No empirical experiments or research dossiers linked to this project.")
            out.append("  - `[AI RECOMMENDATION]` If technical feasibility is untested, link a formal hypothesis test.")

        out.append("\n### 3. Risk & Dependency Analysis")
        blocked_tasks = [t for t in tasks if t.status.value == "blocked"]
        if blocked_tasks:
            for b in blocked_tasks:
                out.append(f"- `[FACT]` Critical Bottleneck: `{b.title}` is blocked.")
                out.append(f"  - `[USER CONTEXT]` Blocker Details: {b.blocker_reason}")
                out.append(f"  - `[AI RECOMMENDATION]` Resolve this blocker before committing new feature work.")
        else:
            out.append("- `[FACT]` No internal tasks currently marked as blocked.")

        out.append("\n### 4. Immediate Tactical Recommendations")
        if project.next_actions:
            for idx, act in enumerate(project.next_actions, 1):
                out.append(f"{idx}. `[USER CONTEXT]` Prioritized Action: {act}")
        else:
            out.append("1. `[AI RECOMMENDATION]` Define explicit task breakdown in Today cockpit.")
            out.append("2. `[AI RECOMMENDATION]` Validate architectural dependencies.")

        return "\n".join(out)

    # --- 4. IDEA ANALYSIS ---
    @staticmethod
    def analyze_idea(idea_id: str) -> str:
        idea = Repository.get_idea(idea_id)
        if not idea:
            return f"Idea with ID '{idea_id}' not found."

        experiments = [e for e in Repository.get_experiments() if e.idea_id == idea_id]

        system_instruction = (
            "You are a Venture Partner and Applied AI Scientist. Stress-test this idea. "
            "Tag strictly with [FACT], [USER CONTEXT], [ASSUMPTION], [AI RECOMMENDATION]."
        )
        user_prompt = f"""
Idea: {idea.title}
Category: {idea.category.value}
Current Stage: {idea.status.value}
Priority: {idea.priority.value}
Origin: {idea.origin}
Description: {idea.description}
Next Action: {idea.next_action}
Attached Experiments: {[e.title for e in experiments]}

Deconstruct:
1. Problem Sharpness & Value Proposition
2. Critical Unvalidated Assumptions
3. Competing Alternatives & Failure Modes
4. Recommended Validation Experiment Design
"""
        llm_result = AIService._call_gemini_if_available(user_prompt, system_instruction)
        if llm_result:
            return llm_result

        out = []
        out.append(f"# 💡 Idea Stress-Test: {idea.title}\n")
        out.append("### 1. Problem Sharpness & Core Value")
        out.append(f"- `[FACT]` Current Pipeline Stage: **{idea.status.value.upper()}** (Category: {idea.category.value})")
        out.append(f"- `[USER CONTEXT]` Origin: {idea.origin or 'Unspecified'}")
        out.append(f"- `[USER CONTEXT]` Description: {idea.description or 'No detailed description provided'}")

        out.append("\n### 2. Critical Unvalidated Assumptions")
        out.append("- `[ASSUMPTION]` **Adoption Demand**: End users experience acute pain under the status quo and will adopt this workflow.")
        out.append("- `[ASSUMPTION]` **Technical Viability**: Performance and inference costs can be kept within sustainable operational envelopes.")
        out.append("- `[ASSUMPTION]` **Defensibility**: The solution provides durable differentiation beyond standard foundation model capabilities.")

        out.append("\n### 3. Failure Modes & Competitive Counter-Forces")
        out.append("- `[ASSUMPTION]` **Commoditization Risk**: Native platform updates may render specialized custom glue obsolete.")
        out.append("- `[ASSUMPTION]` **Execution Friction**: High implementation complexity could delay time-to-value.")

        out.append("\n### 4. Proposed Validation Experiment (Idea -> Test)")
        if experiments:
            out.append(f"- `[FACT]` An experiment is already registered: **{experiments[0].title}** (Status: {experiments[0].status.value})")
            out.append(f"  - `[FACT]` Hypothesis: {experiments[0].hypothesis}")
            out.append(f"  - `[AI RECOMMENDATION]` Complete execution of this experiment before transitioning idea to `planned`.")
        else:
            out.append(f"- `[AI RECOMMENDATION]` **Formulate Minimum Viable Test**:")
            out.append(f"  - **Hypothesis**: If we build a prototype of {idea.title}, we will achieve benchmark verification within 5 working days.")
            out.append(f"  - **Metric**: Measure latency, throughput, or user conversion against baseline.")
            out.append(f"  - **Next Step**: Click 'New Experiment' in the HUD to register this test.")

        return "\n".join(out)

    # --- 5. DECISION REVIEW ---
    @staticmethod
    def review_decision(decision_id: str) -> str:
        dec = Repository.get_decision(decision_id)
        if not dec:
            return f"Decision with ID '{decision_id}' not found."

        system_instruction = (
            "You are a Decision Intelligence Scientist analyzing cognitive calibration and retrospective outcomes. "
            "Tag strictly with [FACT], [USER CONTEXT], [ASSUMPTION], [AI RECOMMENDATION]."
        )
        user_prompt = f"""
Decision: {dec.title}
Date: {dec.date}
Context: {dec.context}
Alternatives Considered: {[a.option for a in dec.alternatives_considered]}
Assumptions: {dec.assumptions}
Evidence: {dec.evidence}
Expected Outcome: {dec.expected_outcome}
Actual Outcome: {dec.actual_outcome}
Confidence Level: {dec.confidence_level}%
Lessons Learned: {dec.lessons_learned}

Analyze:
1. Decision Context & Calibration Audit
2. Expected vs. Actual Outcome Comparison
3. Cognitive Biases & Blindspots Detected
4. Actionable Heuristics for Future Decisions
"""
        llm_result = AIService._call_gemini_if_available(user_prompt, system_instruction)
        if llm_result:
            return llm_result

        out = []
        out.append(f"# ⚖️ Decision Retrospective Audit: {dec.title}\n")
        out.append("### 1. Calibration & Baseline Audit")
        out.append(f"- `[FACT]` Date of Decision: **{dec.date}** | Initial Confidence: **{dec.confidence_level}%**")
        out.append(f"- `[USER CONTEXT]` Decision Context: {dec.context}")
        out.append(f"- `[USER CONTEXT]` Alternatives Considered: {len(dec.alternatives_considered)} options recorded.")
        for alt in dec.alternatives_considered:
            out.append(f"  - Option: `{alt.option}` (Pros: {alt.pros} | Cons: {alt.cons})")

        out.append("\n### 2. Expected vs. Actual Outcomes")
        out.append(f"- `[USER CONTEXT]` **Predicted Outcome**: {dec.expected_outcome}")
        if dec.actual_outcome:
            out.append(f"- `[USER CONTEXT]` **Recorded Actual Outcome**: {dec.actual_outcome}")
            if dec.confidence_level >= 80:
                out.append("- `[AI RECOMMENDATION]` **Calibration Check**: High confidence matched with recorded outcome. Audit whether assumptions held true.")
        else:
            out.append("- `[FACT]` **Actual outcome has not been logged yet**.")
            out.append("  - `[AI RECOMMENDATION]` Log empirical results in the Decision Log once verified.")

        out.append("\n### 3. Underlying Assumptions & Vulnerabilities")
        out.append(f"- `[USER CONTEXT]` Stated Assumptions: {dec.assumptions}")
        out.append(f"- `[USER CONTEXT]` Stated Evidence: {dec.evidence}")
        if not dec.evidence or len(dec.evidence.strip()) < 15:
            out.append("- `[ASSUMPTION]` **Low Evidence Base**: Decision relied heavily on intuition rather than empirical benchmarks.")

        out.append("\n### 4. Meta-Lessons & Tactical Takeaways")
        if dec.lessons_learned:
            out.append(f"- `[USER CONTEXT]` Logged Lessons: {dec.lessons_learned}")
        else:
            out.append("- `[AI RECOMMENDATION]` Record lessons learned to update your personal decision database.")

        return "\n".join(out)
