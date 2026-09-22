# Pydantic Schema & Data Types Reference

This document catalogs the Pydantic v2 schemas and enumerations defined in `app/models.py`.

---

## 1. Enumeration Types

| Enum Name | Allowed Values |
|---|---|
| `TaskPriority` | `p0_critical`, `p1_high`, `p2_medium`, `p3_low` |
| `TaskStatus` | `todo`, `in_progress`, `blocked`, `completed` |
| `EnergyLevel` | `deep_work`, `quick_win`, `administrative` |
| `ProjectCategory` | `ai_systems`, `research`, `product`, `career`, `infrastructure` |
| `ProjectStatus` | `active`, `planned`, `completed`, `blocked`, `maintenance` |
| `ProjectHealth` | `green`, `yellow`, `red` |
| `IdeaCategory` | `software`, `research`, `venture`, `content`, `personal` |
| `IdeaStatus` | `captured`, `explored`, `validated`, `planned`, `executing`, `completed`, `abandoned` |
| `IdeaPriority` | `high`, `medium`, `low` |
| `ExperimentStatus` | `hypothesis`, `design`, `running`, `analyzing`, `concluded`, `aborted` |
| `DecisionStatus` | `pending_review`, `reviewed`, `superseded` |
| `ResearchStatus` | `exploring`, `synthesizing`, `concluded`, `dormant` |
| `LearningType` | `book`, `course`, `paper`, `tutorial`, `topic` |
| `LearningStatus` | `queued`, `active`, `paused`, `completed` |
| `OpportunityCategory` | `technology`, `career`, `business`, `entrepreneurship`, `education`, `investment`, `consulting`, `partnerships`, `emerging_markets` |
| `OpportunityStatus` | `evaluating`, `pursuing`, `watching`, `archived` |
| `RelationType` | `leads_to`, `validates`, `informs`, `implements`, `spawns`, `depends_on`, `references` |

---

## 2. Core Entity Schemas

### 2.1 Task Schemas
```python
class TaskBase(BaseModel):
    title: str
    project_id: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.p2_medium
    deadline: Optional[str] = None
    scheduled_date: Optional[str] = None
    blocker_reason: Optional[str] = None
    energy_level: EnergyLevel = EnergyLevel.deep_work
    tags: List[str] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    project_id: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    deadline: Optional[str] = None
    scheduled_date: Optional[str] = None
    blocker_reason: Optional[str] = None
    energy_level: Optional[EnergyLevel] = None
    tags: Optional[List[str]] = None

class Task(TaskBase):
    id: str
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
```

### 2.2 Project Schemas
```python
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = ""
    category: ProjectCategory = ProjectCategory.ai_systems
    status: ProjectStatus = ProjectStatus.active
    health: ProjectHealth = ProjectHealth.green
    progress_pct: int = Field(default=0, ge=0, le=100)
    next_actions: List[str] = []
    target_date: Optional[str] = None

class Project(ProjectBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.3 Idea Schemas
```python
class IdeaBase(BaseModel):
    title: str
    description: Optional[str] = ""
    category: IdeaCategory = IdeaCategory.software
    origin: Optional[str] = ""
    status: IdeaStatus = IdeaStatus.captured
    priority: IdeaPriority = IdeaPriority.medium
    next_action: Optional[str] = ""
    related_project_id: Optional[str] = None

class Idea(IdeaBase):
    id: str
    created_at: str
    updated_at: str
    status_changed_at: str
```

### 2.4 Experiment Schemas
```python
class ExperimentBase(BaseModel):
    idea_id: Optional[str] = None
    project_id: Optional[str] = None
    title: str
    hypothesis: str
    objective: str
    assumptions: List[str] = []
    experiment_design: str
    expected_result: str
    actual_result: Optional[str] = ""
    evidence: Optional[str] = ""
    conclusion: Optional[str] = ""
    next_step: Optional[str] = ""
    status: ExperimentStatus = ExperimentStatus.hypothesis

class Experiment(ExperimentBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.5 Decision Schemas
```python
class DecisionAlternative(BaseModel):
    option: str
    pros: str = ""
    cons: str = ""

class DecisionBase(BaseModel):
    title: str
    date: str
    context: str
    alternatives_considered: List[DecisionAlternative] = []
    assumptions: str
    evidence: str
    expected_outcome: str
    actual_outcome: Optional[str] = ""
    confidence_level: int = Field(default=75, ge=1, le=100)
    lessons_learned: Optional[str] = ""
    status: DecisionStatus = DecisionStatus.pending_review
    review_date: Optional[str] = None

class Decision(DecisionBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.6 Research Schemas
```python
class ResearchFinding(BaseModel):
    claim: str
    evidence: str = ""
    confidence: str = "high"

class ResearchSource(BaseModel):
    title: str
    url_or_citation: str
    type: str = "paper"

class ResearchEntryBase(BaseModel):
    research_question: str
    topic: str
    status: ResearchStatus = ResearchStatus.exploring
    investigations: Optional[str] = ""
    findings: List[ResearchFinding] = []
    sources: List[ResearchSource] = []
    conclusions: Optional[str] = ""
    unresolved_questions: List[str] = []
    related_project_id: Optional[str] = None

class ResearchEntry(ResearchEntryBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.7 Learning Schemas
```python
class PracticalExercise(BaseModel):
    title: str
    completed: bool = False

class LearningItemBase(BaseModel):
    subject: str
    title: str
    type: LearningType = LearningType.book
    progress_pct: int = Field(default=0, ge=0, le=100)
    status: LearningStatus = LearningStatus.active
    notes: Optional[str] = ""
    practical_exercises: List[PracticalExercise] = []
    key_takeaways: Optional[str] = ""

class LearningItem(LearningItemBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.8 Opportunity Schemas
```python
class OpportunityBase(BaseModel):
    title: str
    description: Optional[str] = ""
    source: Optional[str] = ""
    date_discovered: str
    category: OpportunityCategory = OpportunityCategory.technology
    potential_upside: Optional[str] = ""
    requirements: Optional[str] = ""
    risks: Optional[str] = ""
    status: OpportunityStatus = OpportunityStatus.evaluating
    next_action: Optional[str] = ""

class Opportunity(OpportunityBase):
    id: str
    created_at: str
    updated_at: str
```

### 2.9 Knowledge Edge Schemas
```python
class KnowledgeEdgeCreate(BaseModel):
    source_type: str
    source_id: str
    target_type: str
    target_id: str
    relation_type: RelationType
    notes: Optional[str] = ""

class KnowledgeEdge(KnowledgeEdgeCreate):
    id: str
    created_at: str
```

---

## 3. Aggregate View Schemas

### 3.1 Graph Data Schemas
```python
class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    subtitle: Optional[str] = ""
    status: Optional[str] = ""
    health: Optional[str] = None
    data: Dict[str, Any] = {}

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relation: str
    notes: Optional[str] = ""

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
```

### 3.2 Search Result Schema
```python
class SearchResultItem(BaseModel):
    id: str
    entity_type: str
    title: str
    subtitle: str
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    snippet: str
    date: Optional[str] = None
    tags: List[str] = []
    relevance_score: float = 1.0
```

### 3.3 Situational Metrics Schema
```python
class SituationalMetrics(BaseModel):
    active_projects: int
    completed_projects: int
    stalled_projects: int
    overdue_tasks: int
    critical_p0_tasks: int
    blocked_tasks: int
    ideas_captured: int
    ideas_validated: int
    ideas_in_flight: int
    experiments_running: int
    experiments_concluded: int
    decisions_logged: int
    decisions_pending_review: int
    active_learning_items: int
    opportunities_discovered: int
    opportunities_pursuing: int
    project_health_breakdown: Dict[str, int]
    idea_funnel_breakdown: Dict[str, int]
    stagnation_alerts: List[Dict[str, Any]]
```
