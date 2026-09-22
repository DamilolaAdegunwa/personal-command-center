import json
import uuid
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from app.database import get_connection
from app.models import (
    Task, TaskCreate, TaskUpdate, TaskStatus,
    Project, ProjectCreate, ProjectUpdate,
    Idea, IdeaCreate, IdeaUpdate, IdeaStatus,
    Experiment, ExperimentCreate, ExperimentUpdate,
    Decision, DecisionCreate, DecisionUpdate,
    ResearchEntry, ResearchEntryCreate, ResearchEntryUpdate,
    LearningItem, LearningItemCreate, LearningItemUpdate,
    Opportunity, OpportunityCreate, OpportunityUpdate,
    KnowledgeEdge, KnowledgeEdgeCreate
)

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class Repository:
    # --- TASKS ---
    @staticmethod
    def get_tasks(
        status: Optional[str] = None,
        priority: Optional[str] = None,
        project_id: Optional[str] = None
    ) -> List[Task]:
        conn = get_connection()
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        if project_id:
            query += " AND project_id = ?"
            params.append(project_id)
        query += " ORDER BY CASE priority WHEN 'p0_critical' THEN 0 WHEN 'p1_high' THEN 1 WHEN 'p2_medium' THEN 2 ELSE 3 END, deadline ASC, created_at DESC"
        
        rows = conn.execute(query, params).fetchall()
        tasks = []
        for r in rows:
            tasks.append(Task(
                id=r["id"],
                title=r["title"],
                project_id=r["project_id"],
                status=r["status"],
                priority=r["priority"],
                deadline=r["deadline"],
                scheduled_date=r["scheduled_date"],
                blocker_reason=r["blocker_reason"],
                energy_level=r["energy_level"],
                tags=json.loads(r["tags"] or "[]"),
                created_at=r["created_at"],
                updated_at=r["updated_at"],
                completed_at=r["completed_at"]
            ))
        conn.close()
        return tasks

    @staticmethod
    def get_task(task_id: str) -> Optional[Task]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Task(
            id=r["id"],
            title=r["title"],
            project_id=r["project_id"],
            status=r["status"],
            priority=r["priority"],
            deadline=r["deadline"],
            scheduled_date=r["scheduled_date"],
            blocker_reason=r["blocker_reason"],
            energy_level=r["energy_level"],
            tags=json.loads(r["tags"] or "[]"),
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            completed_at=r["completed_at"]
        )

    @staticmethod
    def create_task(data: TaskCreate) -> Task:
        conn = get_connection()
        t_id = str(uuid.uuid4())
        ts = now_iso()
        completed_at = ts if data.status == TaskStatus.completed else None
        conn.execute(
            """INSERT INTO tasks (id, title, project_id, status, priority, deadline, scheduled_date, blocker_reason, energy_level, tags, created_at, updated_at, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (t_id, data.title, data.project_id, data.status.value, data.priority.value, data.deadline,
             data.scheduled_date, data.blocker_reason, data.energy_level.value, json.dumps(data.tags),
             ts, ts, completed_at)
        )
        conn.commit()
        conn.close()
        return Repository.get_task(t_id)

    @staticmethod
    def update_task(task_id: str, data: TaskUpdate) -> Optional[Task]:
        task = Repository.get_task(task_id)
        if not task:
            return None
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        
        if data.title is not None:
            fields.append("title = ?"); params.append(data.title)
        if data.project_id is not None:
            fields.append("project_id = ?"); params.append(data.project_id)
        if data.status is not None:
            fields.append("status = ?"); params.append(data.status.value)
            if data.status == TaskStatus.completed and not task.completed_at:
                fields.append("completed_at = ?"); params.append(ts)
            elif data.status != TaskStatus.completed:
                fields.append("completed_at = ?"); params.append(None)
        if data.priority is not None:
            fields.append("priority = ?"); params.append(data.priority.value)
        if data.deadline is not None:
            fields.append("deadline = ?"); params.append(data.deadline)
        if data.scheduled_date is not None:
            fields.append("scheduled_date = ?"); params.append(data.scheduled_date)
        if data.blocker_reason is not None:
            fields.append("blocker_reason = ?"); params.append(data.blocker_reason)
        if data.energy_level is not None:
            fields.append("energy_level = ?"); params.append(data.energy_level.value)
        if data.tags is not None:
            fields.append("tags = ?"); params.append(json.dumps(data.tags))

        fields.append("updated_at = ?"); params.append(ts)
        params.append(task_id)

        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_task(task_id)

    @staticmethod
    def delete_task(task_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- PROJECTS ---
    @staticmethod
    def get_projects(status: Optional[str] = None, health: Optional[str] = None) -> List[Project]:
        conn = get_connection()
        query = "SELECT * FROM projects WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if health:
            query += " AND health = ?"
            params.append(health)
        query += " ORDER BY target_date ASC, updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        projects = []
        for r in rows:
            projects.append(Project(
                id=r["id"],
                title=r["title"],
                description=r["description"] or "",
                category=r["category"],
                status=r["status"],
                health=r["health"],
                progress_pct=r["progress_pct"],
                next_actions=json.loads(r["next_actions"] or "[]"),
                target_date=r["target_date"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return projects

    @staticmethod
    def get_project(project_id: str) -> Optional[Project]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Project(
            id=r["id"],
            title=r["title"],
            description=r["description"] or "",
            category=r["category"],
            status=r["status"],
            health=r["health"],
            progress_pct=r["progress_pct"],
            next_actions=json.loads(r["next_actions"] or "[]"),
            target_date=r["target_date"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_project(data: ProjectCreate) -> Project:
        conn = get_connection()
        p_id = str(uuid.uuid4())
        ts = now_iso()
        conn.execute(
            """INSERT INTO projects (id, title, description, category, status, health, progress_pct, next_actions, target_date, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (p_id, data.title, data.description, data.category.value, data.status.value,
             data.health.value, data.progress_pct, json.dumps(data.next_actions), data.target_date, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_project(p_id)

    @staticmethod
    def update_project(project_id: str, data: ProjectUpdate) -> Optional[Project]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.title is not None:
            fields.append("title = ?"); params.append(data.title)
        if data.description is not None:
            fields.append("description = ?"); params.append(data.description)
        if data.category is not None:
            fields.append("category = ?"); params.append(data.category.value)
        if data.status is not None:
            fields.append("status = ?"); params.append(data.status.value)
        if data.health is not None:
            fields.append("health = ?"); params.append(data.health.value)
        if data.progress_pct is not None:
            fields.append("progress_pct = ?"); params.append(data.progress_pct)
        if data.next_actions is not None:
            fields.append("next_actions = ?"); params.append(json.dumps(data.next_actions))
        if data.target_date is not None:
            fields.append("target_date = ?"); params.append(data.target_date)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(project_id)
        conn.execute(f"UPDATE projects SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_project(project_id)

    @staticmethod
    def delete_project(project_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- IDEAS ---
    @staticmethod
    def get_ideas(status: Optional[str] = None, category: Optional[str] = None) -> List[Idea]:
        conn = get_connection()
        query = "SELECT * FROM ideas WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " ORDER BY updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        ideas = []
        for r in rows:
            ideas.append(Idea(
                id=r["id"],
                title=r["title"],
                description=r["description"] or "",
                category=r["category"],
                origin=r["origin"] or "",
                status=r["status"],
                priority=r["priority"],
                next_action=r["next_action"] or "",
                related_project_id=r["related_project_id"],
                created_at=r["created_at"],
                updated_at=r["updated_at"],
                status_changed_at=r["status_changed_at"]
            ))
        conn.close()
        return ideas

    @staticmethod
    def get_idea(idea_id: str) -> Optional[Idea]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM ideas WHERE id = ?", (idea_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Idea(
            id=r["id"],
            title=r["title"],
            description=r["description"] or "",
            category=r["category"],
            origin=r["origin"] or "",
            status=r["status"],
            priority=r["priority"],
            next_action=r["next_action"] or "",
            related_project_id=r["related_project_id"],
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            status_changed_at=r["status_changed_at"]
        )

    @staticmethod
    def create_idea(data: IdeaCreate) -> Idea:
        conn = get_connection()
        i_id = str(uuid.uuid4())
        ts = now_iso()
        conn.execute(
            """INSERT INTO ideas (id, title, description, category, origin, status, priority, next_action, related_project_id, created_at, updated_at, status_changed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (i_id, data.title, data.description, data.category.value, data.origin,
             data.status.value, data.priority.value, data.next_action, data.related_project_id, ts, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_idea(i_id)

    @staticmethod
    def update_idea(idea_id: str, data: IdeaUpdate) -> Optional[Idea]:
        existing = Repository.get_idea(idea_id)
        if not existing:
            return None
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.title is not None:
            fields.append("title = ?"); params.append(data.title)
        if data.description is not None:
            fields.append("description = ?"); params.append(data.description)
        if data.category is not None:
            fields.append("category = ?"); params.append(data.category.value)
        if data.origin is not None:
            fields.append("origin = ?"); params.append(data.origin)
        if data.status is not None:
            fields.append("status = ?"); params.append(data.status.value)
            if data.status != existing.status:
                fields.append("status_changed_at = ?"); params.append(ts)
        if data.priority is not None:
            fields.append("priority = ?"); params.append(data.priority.value)
        if data.next_action is not None:
            fields.append("next_action = ?"); params.append(data.next_action)
        if data.related_project_id is not None:
            fields.append("related_project_id = ?"); params.append(data.related_project_id)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(idea_id)
        conn.execute(f"UPDATE ideas SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_idea(idea_id)

    @staticmethod
    def delete_idea(idea_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- EXPERIMENTS ---
    @staticmethod
    def get_experiments(status: Optional[str] = None) -> List[Experiment]:
        conn = get_connection()
        query = "SELECT * FROM experiments WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        experiments = []
        for r in rows:
            experiments.append(Experiment(
                id=r["id"],
                idea_id=r["idea_id"],
                project_id=r["project_id"],
                title=r["title"],
                hypothesis=r["hypothesis"],
                objective=r["objective"],
                assumptions=json.loads(r["assumptions"] or "[]"),
                experiment_design=r["experiment_design"],
                expected_result=r["expected_result"],
                actual_result=r["actual_result"] or "",
                evidence=r["evidence"] or "",
                conclusion=r["conclusion"] or "",
                next_step=r["next_step"] or "",
                status=r["status"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return experiments

    @staticmethod
    def get_experiment(exp_id: str) -> Optional[Experiment]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM experiments WHERE id = ?", (exp_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Experiment(
            id=r["id"],
            idea_id=r["idea_id"],
            project_id=r["project_id"],
            title=r["title"],
            hypothesis=r["hypothesis"],
            objective=r["objective"],
            assumptions=json.loads(r["assumptions"] or "[]"),
            experiment_design=r["experiment_design"],
            expected_result=r["expected_result"],
            actual_result=r["actual_result"] or "",
            evidence=r["evidence"] or "",
            conclusion=r["conclusion"] or "",
            next_step=r["next_step"] or "",
            status=r["status"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_experiment(data: ExperimentCreate) -> Experiment:
        conn = get_connection()
        e_id = str(uuid.uuid4())
        ts = now_iso()
        conn.execute(
            """INSERT INTO experiments (id, idea_id, project_id, title, hypothesis, objective, assumptions, experiment_design, expected_result, actual_result, evidence, conclusion, next_step, status, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (e_id, data.idea_id, data.project_id, data.title, data.hypothesis, data.objective,
             json.dumps(data.assumptions), data.experiment_design, data.expected_result,
             data.actual_result, data.evidence, data.conclusion, data.next_step, data.status.value, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_experiment(e_id)

    @staticmethod
    def update_experiment(exp_id: str, data: ExperimentUpdate) -> Optional[Experiment]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.idea_id is not None: fields.append("idea_id = ?"); params.append(data.idea_id)
        if data.project_id is not None: fields.append("project_id = ?"); params.append(data.project_id)
        if data.title is not None: fields.append("title = ?"); params.append(data.title)
        if data.hypothesis is not None: fields.append("hypothesis = ?"); params.append(data.hypothesis)
        if data.objective is not None: fields.append("objective = ?"); params.append(data.objective)
        if data.assumptions is not None: fields.append("assumptions = ?"); params.append(json.dumps(data.assumptions))
        if data.experiment_design is not None: fields.append("experiment_design = ?"); params.append(data.experiment_design)
        if data.expected_result is not None: fields.append("expected_result = ?"); params.append(data.expected_result)
        if data.actual_result is not None: fields.append("actual_result = ?"); params.append(data.actual_result)
        if data.evidence is not None: fields.append("evidence = ?"); params.append(data.evidence)
        if data.conclusion is not None: fields.append("conclusion = ?"); params.append(data.conclusion)
        if data.next_step is not None: fields.append("next_step = ?"); params.append(data.next_step)
        if data.status is not None: fields.append("status = ?"); params.append(data.status.value)
        
        fields.append("updated_at = ?"); params.append(ts)
        params.append(exp_id)
        conn.execute(f"UPDATE experiments SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_experiment(exp_id)

    @staticmethod
    def delete_experiment(exp_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM experiments WHERE id = ?", (exp_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- DECISIONS ---
    @staticmethod
    def get_decisions(status: Optional[str] = None) -> List[Decision]:
        conn = get_connection()
        query = "SELECT * FROM decisions WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY date DESC, created_at DESC"
        rows = conn.execute(query, params).fetchall()
        decisions = []
        for r in rows:
            decisions.append(Decision(
                id=r["id"],
                title=r["title"],
                date=r["date"],
                context=r["context"],
                alternatives_considered=json.loads(r["alternatives_considered"] or "[]"),
                assumptions=r["assumptions"],
                evidence=r["evidence"],
                expected_outcome=r["expected_outcome"],
                actual_outcome=r["actual_outcome"] or "",
                confidence_level=r["confidence_level"],
                lessons_learned=r["lessons_learned"] or "",
                status=r["status"],
                review_date=r["review_date"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return decisions

    @staticmethod
    def get_decision(d_id: str) -> Optional[Decision]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM decisions WHERE id = ?", (d_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Decision(
            id=r["id"],
            title=r["title"],
            date=r["date"],
            context=r["context"],
            alternatives_considered=json.loads(r["alternatives_considered"] or "[]"),
            assumptions=r["assumptions"],
            evidence=r["evidence"],
            expected_outcome=r["expected_outcome"],
            actual_outcome=r["actual_outcome"] or "",
            confidence_level=r["confidence_level"],
            lessons_learned=r["lessons_learned"] or "",
            status=r["status"],
            review_date=r["review_date"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_decision(data: DecisionCreate) -> Decision:
        conn = get_connection()
        d_id = str(uuid.uuid4())
        ts = now_iso()
        alts = [a.model_dump() for a in data.alternatives_considered]
        conn.execute(
            """INSERT INTO decisions (id, title, date, context, alternatives_considered, assumptions, evidence, expected_outcome, actual_outcome, confidence_level, lessons_learned, status, review_date, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (d_id, data.title, data.date, data.context, json.dumps(alts), data.assumptions, data.evidence,
             data.expected_outcome, data.actual_outcome, data.confidence_level, data.lessons_learned,
             data.status.value, data.review_date, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_decision(d_id)

    @staticmethod
    def update_decision(d_id: str, data: DecisionUpdate) -> Optional[Decision]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.title is not None: fields.append("title = ?"); params.append(data.title)
        if data.date is not None: fields.append("date = ?"); params.append(data.date)
        if data.context is not None: fields.append("context = ?"); params.append(data.context)
        if data.alternatives_considered is not None:
            alts = [a.model_dump() for a in data.alternatives_considered]
            fields.append("alternatives_considered = ?"); params.append(json.dumps(alts))
        if data.assumptions is not None: fields.append("assumptions = ?"); params.append(data.assumptions)
        if data.evidence is not None: fields.append("evidence = ?"); params.append(data.evidence)
        if data.expected_outcome is not None: fields.append("expected_outcome = ?"); params.append(data.expected_outcome)
        if data.actual_outcome is not None: fields.append("actual_outcome = ?"); params.append(data.actual_outcome)
        if data.confidence_level is not None: fields.append("confidence_level = ?"); params.append(data.confidence_level)
        if data.lessons_learned is not None: fields.append("lessons_learned = ?"); params.append(data.lessons_learned)
        if data.status is not None: fields.append("status = ?"); params.append(data.status.value)
        if data.review_date is not None: fields.append("review_date = ?"); params.append(data.review_date)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(d_id)
        conn.execute(f"UPDATE decisions SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_decision(d_id)

    @staticmethod
    def delete_decision(d_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM decisions WHERE id = ?", (d_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- RESEARCH ENTRIES ---
    @staticmethod
    def get_research_entries(topic: Optional[str] = None, status: Optional[str] = None) -> List[ResearchEntry]:
        conn = get_connection()
        query = "SELECT * FROM research_entries WHERE 1=1"
        params = []
        if topic:
            query += " AND topic = ?"
            params.append(topic)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        entries = []
        for r in rows:
            entries.append(ResearchEntry(
                id=r["id"],
                research_question=r["research_question"],
                topic=r["topic"],
                status=r["status"],
                investigations=r["investigations"] or "",
                findings=json.loads(r["findings"] or "[]"),
                sources=json.loads(r["sources"] or "[]"),
                conclusions=r["conclusions"] or "",
                unresolved_questions=json.loads(r["unresolved_questions"] or "[]"),
                related_project_id=r["related_project_id"],
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return entries

    @staticmethod
    def get_research_entry(res_id: str) -> Optional[ResearchEntry]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM research_entries WHERE id = ?", (res_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return ResearchEntry(
            id=r["id"],
            research_question=r["research_question"],
            topic=r["topic"],
            status=r["status"],
            investigations=r["investigations"] or "",
            findings=json.loads(r["findings"] or "[]"),
            sources=json.loads(r["sources"] or "[]"),
            conclusions=r["conclusions"] or "",
            unresolved_questions=json.loads(r["unresolved_questions"] or "[]"),
            related_project_id=r["related_project_id"],
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_research_entry(data: ResearchEntryCreate) -> ResearchEntry:
        conn = get_connection()
        r_id = str(uuid.uuid4())
        ts = now_iso()
        findings = [f.model_dump() for f in data.findings]
        sources = [s.model_dump() for s in data.sources]
        conn.execute(
            """INSERT INTO research_entries (id, research_question, topic, status, investigations, findings, sources, conclusions, unresolved_questions, related_project_id, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (r_id, data.research_question, data.topic, data.status.value, data.investigations,
             json.dumps(findings), json.dumps(sources), data.conclusions,
             json.dumps(data.unresolved_questions), data.related_project_id, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_research_entry(r_id)

    @staticmethod
    def update_research_entry(res_id: str, data: ResearchEntryUpdate) -> Optional[ResearchEntry]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.research_question is not None: fields.append("research_question = ?"); params.append(data.research_question)
        if data.topic is not None: fields.append("topic = ?"); params.append(data.topic)
        if data.status is not None: fields.append("status = ?"); params.append(data.status.value)
        if data.investigations is not None: fields.append("investigations = ?"); params.append(data.investigations)
        if data.findings is not None:
            findings = [f.model_dump() for f in data.findings]
            fields.append("findings = ?"); params.append(json.dumps(findings))
        if data.sources is not None:
            sources = [s.model_dump() for s in data.sources]
            fields.append("sources = ?"); params.append(json.dumps(sources))
        if data.conclusions is not None: fields.append("conclusions = ?"); params.append(data.conclusions)
        if data.unresolved_questions is not None:
            fields.append("unresolved_questions = ?"); params.append(json.dumps(data.unresolved_questions))
        if data.related_project_id is not None: fields.append("related_project_id = ?"); params.append(data.related_project_id)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(res_id)
        conn.execute(f"UPDATE research_entries SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_research_entry(res_id)

    @staticmethod
    def delete_research_entry(res_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM research_entries WHERE id = ?", (res_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- LEARNING ITEMS ---
    @staticmethod
    def get_learning_items(status: Optional[str] = None) -> List[LearningItem]:
        conn = get_connection()
        query = "SELECT * FROM learning_items WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        items = []
        for r in rows:
            items.append(LearningItem(
                id=r["id"],
                subject=r["subject"],
                title=r["title"],
                type=r["type"],
                progress_pct=r["progress_pct"],
                status=r["status"],
                notes=r["notes"] or "",
                practical_exercises=json.loads(r["practical_exercises"] or "[]"),
                key_takeaways=r["key_takeaways"] or "",
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return items

    @staticmethod
    def get_learning_item(item_id: str) -> Optional[LearningItem]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM learning_items WHERE id = ?", (item_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return LearningItem(
            id=r["id"],
            subject=r["subject"],
            title=r["title"],
            type=r["type"],
            progress_pct=r["progress_pct"],
            status=r["status"],
            notes=r["notes"] or "",
            practical_exercises=json.loads(r["practical_exercises"] or "[]"),
            key_takeaways=r["key_takeaways"] or "",
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_learning_item(data: LearningItemCreate) -> LearningItem:
        conn = get_connection()
        l_id = str(uuid.uuid4())
        ts = now_iso()
        exs = [e.model_dump() for e in data.practical_exercises]
        conn.execute(
            """INSERT INTO learning_items (id, subject, title, type, progress_pct, status, notes, practical_exercises, key_takeaways, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (l_id, data.subject, data.title, data.type.value, data.progress_pct, data.status.value,
             data.notes, json.dumps(exs), data.key_takeaways, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_learning_item(l_id)

    @staticmethod
    def update_learning_item(item_id: str, data: LearningItemUpdate) -> Optional[LearningItem]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.subject is not None: fields.append("subject = ?"); params.append(data.subject)
        if data.title is not None: fields.append("title = ?"); params.append(data.title)
        if data.type is not None: fields.append("type = ?"); params.append(data.type.value)
        if data.progress_pct is not None: fields.append("progress_pct = ?"); params.append(data.progress_pct)
        if data.status is not None: fields.append("status = ?"); params.append(data.status.value)
        if data.notes is not None: fields.append("notes = ?"); params.append(data.notes)
        if data.practical_exercises is not None:
            exs = [e.model_dump() for e in data.practical_exercises]
            fields.append("practical_exercises = ?"); params.append(json.dumps(exs))
        if data.key_takeaways is not None: fields.append("key_takeaways = ?"); params.append(data.key_takeaways)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(item_id)
        conn.execute(f"UPDATE learning_items SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_learning_item(item_id)

    @staticmethod
    def delete_learning_item(item_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM learning_items WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- OPPORTUNITIES ---
    @staticmethod
    def get_opportunities(category: Optional[str] = None, status: Optional[str] = None) -> List[Opportunity]:
        conn = get_connection()
        query = "SELECT * FROM opportunities WHERE 1=1"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY date_discovered DESC, updated_at DESC"
        rows = conn.execute(query, params).fetchall()
        opps = []
        for r in rows:
            opps.append(Opportunity(
                id=r["id"],
                title=r["title"],
                description=r["description"] or "",
                source=r["source"] or "",
                date_discovered=r["date_discovered"],
                category=r["category"],
                potential_upside=r["potential_upside"] or "",
                requirements=r["requirements"] or "",
                risks=r["risks"] or "",
                status=r["status"],
                next_action=r["next_action"] or "",
                created_at=r["created_at"],
                updated_at=r["updated_at"]
            ))
        conn.close()
        return opps

    @staticmethod
    def get_opportunity(opp_id: str) -> Optional[Opportunity]:
        conn = get_connection()
        r = conn.execute("SELECT * FROM opportunities WHERE id = ?", (opp_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return Opportunity(
            id=r["id"],
            title=r["title"],
            description=r["description"] or "",
            source=r["source"] or "",
            date_discovered=r["date_discovered"],
            category=r["category"],
            potential_upside=r["potential_upside"] or "",
            requirements=r["requirements"] or "",
            risks=r["risks"] or "",
            status=r["status"],
            next_action=r["next_action"] or "",
            created_at=r["created_at"],
            updated_at=r["updated_at"]
        )

    @staticmethod
    def create_opportunity(data: OpportunityCreate) -> Opportunity:
        conn = get_connection()
        o_id = str(uuid.uuid4())
        ts = now_iso()
        conn.execute(
            """INSERT INTO opportunities (id, title, description, source, date_discovered, category, potential_upside, requirements, risks, status, next_action, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (o_id, data.title, data.description, data.source, data.date_discovered,
             data.category.value, data.potential_upside, data.requirements, data.risks,
             data.status.value, data.next_action, ts, ts)
        )
        conn.commit()
        conn.close()
        return Repository.get_opportunity(o_id)

    @staticmethod
    def update_opportunity(opp_id: str, data: OpportunityUpdate) -> Optional[Opportunity]:
        conn = get_connection()
        ts = now_iso()
        fields = []
        params = []
        if data.title is not None: fields.append("title = ?"); params.append(data.title)
        if data.description is not None: fields.append("description = ?"); params.append(data.description)
        if data.source is not None: fields.append("source = ?"); params.append(data.source)
        if data.date_discovered is not None: fields.append("date_discovered = ?"); params.append(data.date_discovered)
        if data.category is not None: fields.append("category = ?"); params.append(data.category.value)
        if data.potential_upside is not None: fields.append("potential_upside = ?"); params.append(data.potential_upside)
        if data.requirements is not None: fields.append("requirements = ?"); params.append(data.requirements)
        if data.risks is not None: fields.append("risks = ?"); params.append(data.risks)
        if data.status is not None: fields.append("status = ?"); params.append(data.status.value)
        if data.next_action is not None: fields.append("next_action = ?"); params.append(data.next_action)

        fields.append("updated_at = ?"); params.append(ts)
        params.append(opp_id)
        conn.execute(f"UPDATE opportunities SET {', '.join(fields)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return Repository.get_opportunity(opp_id)

    @staticmethod
    def delete_opportunity(opp_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM opportunities WHERE id = ?", (opp_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0

    # --- KNOWLEDGE EDGES ---
    @staticmethod
    def get_edges(entity_type: Optional[str] = None, entity_id: Optional[str] = None) -> List[KnowledgeEdge]:
        conn = get_connection()
        query = "SELECT * FROM knowledge_edges WHERE 1=1"
        params = []
        if entity_type and entity_id:
            query += " AND ((source_type = ? AND source_id = ?) OR (target_type = ? AND target_id = ?))"
            params.extend([entity_type, entity_id, entity_type, entity_id])
        query += " ORDER BY created_at DESC"
        rows = conn.execute(query, params).fetchall()
        edges = []
        for r in rows:
            edges.append(KnowledgeEdge(
                id=r["id"],
                source_type=r["source_type"],
                source_id=r["source_id"],
                target_type=r["target_type"],
                target_id=r["target_id"],
                relation_type=r["relation_type"],
                notes=r["notes"] or "",
                created_at=r["created_at"]
            ))
        conn.close()
        return edges

    @staticmethod
    def create_edge(data: KnowledgeEdgeCreate) -> KnowledgeEdge:
        conn = get_connection()
        e_id = str(uuid.uuid4())
        ts = now_iso()
        conn.execute(
            """INSERT INTO knowledge_edges (id, source_type, source_id, target_type, target_id, relation_type, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (e_id, data.source_type, data.source_id, data.target_type, data.target_id,
             data.relation_type.value, data.notes, ts)
        )
        conn.commit()
        conn.close()
        return KnowledgeEdge(
            id=e_id,
            source_type=data.source_type,
            source_id=data.source_id,
            target_type=data.target_type,
            target_id=data.target_id,
            relation_type=data.relation_type,
            notes=data.notes,
            created_at=ts
        )

    @staticmethod
    def delete_edge(edge_id: str) -> bool:
        conn = get_connection()
        res = conn.execute("DELETE FROM knowledge_edges WHERE id = ?", (edge_id,))
        conn.commit()
        conn.close()
        return res.rowcount > 0
