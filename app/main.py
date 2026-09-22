import os
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.repository import Repository
from app.models import (
    Task, TaskCreate, TaskUpdate, TaskStatus,
    Project, ProjectCreate, ProjectUpdate,
    Idea, IdeaCreate, IdeaUpdate, IdeaStatus,
    Experiment, ExperimentCreate, ExperimentUpdate,
    Decision, DecisionCreate, DecisionUpdate,
    ResearchEntry, ResearchEntryCreate, ResearchEntryUpdate,
    LearningItem, LearningItemCreate, LearningItemUpdate,
    Opportunity, OpportunityCreate, OpportunityUpdate,
    KnowledgeEdge, KnowledgeEdgeCreate,
    GraphData, SearchResultItem, SituationalMetrics
)
from app.graph_service import GraphService
from app.search_service import SearchService
from app.metrics_service import MetricsService
from app.ai_service import AIService
from app.seed_data import seed_database

from contextlib import asynccontextmanager

# Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_database()
    yield

# Initialize App
app = FastAPI(
    title="Personal Command Center",
    description="A Personal Operating System for an Individual Human Living and Working in the AI Era",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files Path
STATIC_DIR = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return JSONResponse({"message": "Personal Command Center API is online. Static UI build pending."})

@app.get("/api/health")
def healthcheck():
    return {"status": "operational", "system": "Personal Command Center (Personal OS)", "version": "1.0.0"}

# --- 1. TODAY COCKPIT ---
@app.get("/api/today")
def get_today_dashboard():
    tasks = Repository.get_tasks()
    projects = Repository.get_projects(status="active")
    
    p0_critical = [t for t in tasks if t.priority.value == "p0_critical" and t.status.value != "completed"]
    p1_high = [t for t in tasks if t.priority.value == "p1_high" and t.status.value != "completed"]
    blocked = [t for t in tasks if t.status.value == "blocked"]
    in_progress = [t for t in tasks if t.status.value == "in_progress"]
    unfinished = [t for t in tasks if t.status.value in ("todo", "in_progress", "blocked")]
    
    # Deadlines (upcoming in next 7 days or overdue)
    deadlines = [t for t in unfinished if t.deadline]

    return {
        "summary": {
            "active_projects_count": len(projects),
            "p0_count": len(p0_critical),
            "p1_count": len(p1_high),
            "blocked_count": len(blocked),
            "in_progress_count": len(in_progress),
            "unfinished_total": len(unfinished)
        },
        "critical_p0": p0_critical,
        "high_priority_p1": p1_high,
        "blocked_items": blocked,
        "active_work": in_progress,
        "upcoming_deadlines": deadlines,
        "active_projects": projects
    }

# --- 2. PROJECTS ---
@app.get("/api/projects", response_model=List[Project])
def list_projects(status: Optional[str] = None, health: Optional[str] = None):
    return Repository.get_projects(status=status, health=health)

@app.post("/api/projects", response_model=Project)
def create_project(data: ProjectCreate):
    return Repository.create_project(data)

@app.get("/api/projects/{project_id}", response_model=Project)
def get_project(project_id: str):
    p = Repository.get_project(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@app.put("/api/projects/{project_id}", response_model=Project)
def update_project(project_id: str, data: ProjectUpdate):
    p = Repository.update_project(project_id, data)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return p

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str):
    if not Repository.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"deleted": True}

# --- 3. IDEAS ---
@app.get("/api/ideas", response_model=List[Idea])
def list_ideas(status: Optional[str] = None, category: Optional[str] = None):
    return Repository.get_ideas(status=status, category=category)

@app.post("/api/ideas", response_model=Idea)
def create_idea(data: IdeaCreate):
    return Repository.create_idea(data)

@app.get("/api/ideas/{idea_id}", response_model=Idea)
def get_idea(idea_id: str):
    i = Repository.get_idea(idea_id)
    if not i:
        raise HTTPException(status_code=404, detail="Idea not found")
    return i

@app.put("/api/ideas/{idea_id}", response_model=Idea)
def update_idea(idea_id: str, data: IdeaUpdate):
    i = Repository.update_idea(idea_id, data)
    if not i:
        raise HTTPException(status_code=404, detail="Idea not found")
    return i

@app.post("/api/ideas/{idea_id}/transition", response_model=Idea)
def transition_idea(idea_id: str, target_status: IdeaStatus):
    i = Repository.update_idea(idea_id, IdeaUpdate(status=target_status))
    if not i:
        raise HTTPException(status_code=404, detail="Idea not found")
    return i

@app.delete("/api/ideas/{idea_id}")
def delete_idea(idea_id: str):
    if not Repository.delete_idea(idea_id):
        raise HTTPException(status_code=404, detail="Idea not found")
    return {"deleted": True}

# --- 4. EXPERIMENTS ---
@app.get("/api/experiments", response_model=List[Experiment])
def list_experiments(status: Optional[str] = None):
    return Repository.get_experiments(status=status)

@app.post("/api/experiments", response_model=Experiment)
def create_experiment(data: ExperimentCreate):
    return Repository.create_experiment(data)

@app.get("/api/experiments/{exp_id}", response_model=Experiment)
def get_experiment(exp_id: str):
    e = Repository.get_experiment(exp_id)
    if not e:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return e

@app.put("/api/experiments/{exp_id}", response_model=Experiment)
def update_experiment(exp_id: str, data: ExperimentUpdate):
    e = Repository.update_experiment(exp_id, data)
    if not e:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return e

@app.delete("/api/experiments/{exp_id}")
def delete_experiment(exp_id: str):
    if not Repository.delete_experiment(exp_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"deleted": True}

# --- 5. DECISIONS ---
@app.get("/api/decisions", response_model=List[Decision])
def list_decisions(status: Optional[str] = None):
    return Repository.get_decisions(status=status)

@app.post("/api/decisions", response_model=Decision)
def create_decision(data: DecisionCreate):
    return Repository.create_decision(data)

@app.get("/api/decisions/{dec_id}", response_model=Decision)
def get_decision(dec_id: str):
    d = Repository.get_decision(dec_id)
    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")
    return d

@app.put("/api/decisions/{dec_id}", response_model=Decision)
def update_decision(dec_id: str, data: DecisionUpdate):
    d = Repository.update_decision(dec_id, data)
    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")
    return d

@app.delete("/api/decisions/{dec_id}")
def delete_decision(dec_id: str):
    if not Repository.delete_decision(dec_id):
        raise HTTPException(status_code=404, detail="Decision not found")
    return {"deleted": True}

# --- 6. RESEARCH ---
@app.get("/api/research", response_model=List[ResearchEntry])
def list_research(topic: Optional[str] = None, status: Optional[str] = None):
    return Repository.get_research_entries(topic=topic, status=status)

@app.post("/api/research", response_model=ResearchEntry)
def create_research(data: ResearchEntryCreate):
    return Repository.create_research_entry(data)

@app.get("/api/research/{res_id}", response_model=ResearchEntry)
def get_research(res_id: str):
    r = Repository.get_research_entry(res_id)
    if not r:
        raise HTTPException(status_code=404, detail="Research entry not found")
    return r

@app.put("/api/research/{res_id}", response_model=ResearchEntry)
def update_research(res_id: str, data: ResearchEntryUpdate):
    r = Repository.update_research_entry(res_id, data)
    if not r:
        raise HTTPException(status_code=404, detail="Research entry not found")
    return r

@app.delete("/api/research/{res_id}")
def delete_research(res_id: str):
    if not Repository.delete_research_entry(res_id):
        raise HTTPException(status_code=404, detail="Research entry not found")
    return {"deleted": True}

# --- 7. LEARNING ---
@app.get("/api/learning", response_model=List[LearningItem])
def list_learning(status: Optional[str] = None):
    return Repository.get_learning_items(status=status)

@app.post("/api/learning", response_model=LearningItem)
def create_learning(data: LearningItemCreate):
    return Repository.create_learning_item(data)

@app.get("/api/learning/{item_id}", response_model=LearningItem)
def get_learning(item_id: str):
    l = Repository.get_learning_item(item_id)
    if not l:
        raise HTTPException(status_code=404, detail="Learning item not found")
    return l

@app.put("/api/learning/{item_id}", response_model=LearningItem)
def update_learning(item_id: str, data: LearningItemUpdate):
    l = Repository.update_learning_item(item_id, data)
    if not l:
        raise HTTPException(status_code=404, detail="Learning item not found")
    return l

@app.delete("/api/learning/{item_id}")
def delete_learning(item_id: str):
    if not Repository.delete_learning_item(item_id):
        raise HTTPException(status_code=404, detail="Learning item not found")
    return {"deleted": True}

# --- 8. OPPORTUNITIES ---
@app.get("/api/opportunities", response_model=List[Opportunity])
def list_opportunities(category: Optional[str] = None, status: Optional[str] = None):
    return Repository.get_opportunities(category=category, status=status)

@app.post("/api/opportunities", response_model=Opportunity)
def create_opportunity(data: OpportunityCreate):
    return Repository.create_opportunity(data)

@app.get("/api/opportunities/{opp_id}", response_model=Opportunity)
def get_opportunity(opp_id: str):
    o = Repository.get_opportunity(opp_id)
    if not o:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return o

@app.put("/api/opportunities/{opp_id}", response_model=Opportunity)
def update_opportunity(opp_id: str, data: OpportunityUpdate):
    o = Repository.update_opportunity(opp_id, data)
    if not o:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return o

@app.delete("/api/opportunities/{opp_id}")
def delete_opportunity(opp_id: str):
    if not Repository.delete_opportunity(opp_id):
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {"deleted": True}

# --- 9. TASKS ---
@app.get("/api/tasks", response_model=List[Task])
def list_tasks(status: Optional[str] = None, priority: Optional[str] = None, project_id: Optional[str] = None):
    return Repository.get_tasks(status=status, priority=priority, project_id=project_id)

@app.post("/api/tasks", response_model=Task)
def create_task(data: TaskCreate):
    return Repository.create_task(data)

@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    t = Repository.get_task(task_id)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t

@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, data: TaskUpdate):
    t = Repository.update_task(task_id, data)
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    return t

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    if not Repository.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}

# --- 10. KNOWLEDGE GRAPH ---
@app.get("/api/graph", response_model=GraphData)
def get_graph():
    return GraphService.get_full_graph()

@app.get("/api/edges", response_model=List[KnowledgeEdge])
def list_edges(entity_type: Optional[str] = None, entity_id: Optional[str] = None):
    return Repository.get_edges(entity_type=entity_type, entity_id=entity_id)

@app.post("/api/edges", response_model=KnowledgeEdge)
def create_edge(data: KnowledgeEdgeCreate):
    return Repository.create_edge(data)

@app.delete("/api/edges/{edge_id}")
def delete_edge(edge_id: str):
    if not Repository.delete_edge(edge_id):
        raise HTTPException(status_code=404, detail="Edge not found")
    return {"deleted": True}

# --- 11. UNIVERSAL OMNI-SEARCH ---
@app.get("/api/search", response_model=List[SearchResultItem])
def search_all(
    q: str = Query("", description="Search keywords"),
    types: Optional[List[str]] = Query(None, description="Entity types to include"),
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 40
):
    return SearchService.search(
        query=q,
        entity_types=types,
        status=status,
        priority=priority,
        tag=tag,
        limit=limit
    )

# --- 12. SITUATIONAL METRICS ---
@app.get("/api/metrics", response_model=SituationalMetrics)
def get_metrics():
    return MetricsService.get_metrics()

# --- 13. GROUNDED AI STUDIO ---
@app.post("/api/ai/daily-briefing")
def get_daily_briefing():
    content = AIService.generate_daily_briefing()
    return {"type": "daily_briefing", "content": content}

@app.post("/api/ai/weekly-review")
def get_weekly_review():
    content = AIService.generate_weekly_review()
    return {"type": "weekly_review", "content": content}

@app.post("/api/ai/analyze-project/{project_id}")
def analyze_project(project_id: str):
    content = AIService.analyze_project(project_id)
    return {"type": "project_analysis", "project_id": project_id, "content": content}

@app.post("/api/ai/analyze-idea/{idea_id}")
def analyze_idea(idea_id: str):
    content = AIService.analyze_idea(idea_id)
    return {"type": "idea_analysis", "idea_id": idea_id, "content": content}

@app.post("/api/ai/review-decision/{decision_id}")
def review_decision(decision_id: str):
    content = AIService.review_decision(decision_id)
    return {"type": "decision_review", "decision_id": decision_id, "content": content}

# --- 14. DATA SEEDING / RESET ---
@app.post("/api/seed")
def reseed_data():
    seed_database()
    return {"status": "success", "message": "Demonstration data initialized."}
