from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List
from app.repository import Repository
from app.models import SituationalMetrics

class MetricsService:
    @staticmethod
    def get_metrics() -> SituationalMetrics:
        now = datetime.now(timezone.utc)
        two_weeks_ago = now - timedelta(days=14)

        # 1. Projects
        projects = Repository.get_projects()
        active_projects = [p for p in projects if p.status.value == "active"]
        completed_projects = [p for p in projects if p.status.value == "completed"]
        
        health_breakdown = {"green": 0, "yellow": 0, "red": 0}
        for p in projects:
            if p.health.value in health_breakdown:
                health_breakdown[p.health.value] += 1

        stalled_projects = []
        for p in active_projects:
            try:
                up_dt = datetime.fromisoformat(p.updated_at)
                if up_dt < two_weeks_ago or p.health.value == "red":
                    stalled_projects.append(p)
            except Exception:
                pass

        # 2. Tasks
        tasks = Repository.get_tasks()
        critical_p0 = [t for t in tasks if t.priority.value == "p0_critical" and t.status.value != "completed"]
        blocked = [t for t in tasks if t.status.value == "blocked"]
        
        overdue_tasks = 0
        for t in tasks:
            if t.status.value != "completed" and t.deadline:
                try:
                    # Parse deadline
                    dl_str = t.deadline
                    if "T" in dl_str:
                        dl_dt = datetime.fromisoformat(dl_str)
                    else:
                        dl_dt = datetime.fromisoformat(dl_str + "T23:59:59+00:00")
                    if dl_dt < now:
                        overdue_tasks += 1
                except Exception:
                    pass

        # 3. Ideas
        ideas = Repository.get_ideas()
        funnel_breakdown = {
            "captured": 0, "explored": 0, "validated": 0,
            "planned": 0, "executing": 0, "completed": 0, "abandoned": 0
        }
        for i in ideas:
            if i.status.value in funnel_breakdown:
                funnel_breakdown[i.status.value] += 1
        
        ideas_captured = len(ideas)
        ideas_validated = funnel_breakdown["validated"] + funnel_breakdown["planned"] + funnel_breakdown["executing"] + funnel_breakdown["completed"]
        ideas_in_flight = funnel_breakdown["planned"] + funnel_breakdown["executing"]

        # 4. Experiments
        exps = Repository.get_experiments()
        experiments_running = len([e for e in exps if e.status.value in ("running", "design")])
        experiments_concluded = len([e for e in exps if e.status.value == "concluded"])

        # 5. Decisions
        decisions = Repository.get_decisions()
        decisions_logged = len(decisions)
        decisions_pending_review = len([d for d in decisions if d.status.value == "pending_review"])

        # 6. Learning
        learning = Repository.get_learning_items()
        active_learning_items = len([l for l in learning if l.status.value == "active"])

        # 7. Opportunities
        opps = Repository.get_opportunities()
        opportunities_discovered = len(opps)
        opportunities_pursuing = len([o for o in opps if o.status.value == "pursuing"])

        # 8. Stagnation Alerts
        stagnation_alerts: List[Dict[str, Any]] = []
        for p in stalled_projects:
            stagnation_alerts.append({
                "type": "project_stagnation",
                "id": p.id,
                "title": p.title,
                "reason": f"Project has red health or no recent updates. Progress at {p.progress_pct}%."
            })
        for b in blocked:
            stagnation_alerts.append({
                "type": "task_blocked",
                "id": b.id,
                "title": b.title,
                "reason": f"Blocked: {b.blocker_reason or 'Dependency stalled'} (Priority: {b.priority.value.upper()})"
            })
        for d in decisions:
            if d.status.value == "pending_review" and d.review_date:
                try:
                    rv_dt = datetime.fromisoformat(d.review_date + "T00:00:00+00:00")
                    if rv_dt <= now:
                        stagnation_alerts.append({
                            "type": "decision_review_due",
                            "id": d.id,
                            "title": d.title,
                            "reason": f"Decision outcome review date ({d.review_date}) has arrived."
                        })
                except Exception:
                    pass

        return SituationalMetrics(
            active_projects=len(active_projects),
            completed_projects=len(completed_projects),
            stalled_projects=len(stalled_projects),
            overdue_tasks=overdue_tasks,
            critical_p0_tasks=len(critical_p0),
            blocked_tasks=len(blocked),
            ideas_captured=ideas_captured,
            ideas_validated=ideas_validated,
            ideas_in_flight=ideas_in_flight,
            experiments_running=experiments_running,
            experiments_concluded=experiments_concluded,
            decisions_logged=decisions_logged,
            decisions_pending_review=decisions_pending_review,
            active_learning_items=active_learning_items,
            opportunities_discovered=opportunities_discovered,
            opportunities_pursuing=opportunities_pursuing,
            project_health_breakdown=health_breakdown,
            idea_funnel_breakdown=funnel_breakdown,
            stagnation_alerts=stagnation_alerts
        )
