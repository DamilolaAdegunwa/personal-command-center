from __future__ import annotations
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timezone

# --- ENUMS ---

class TaskPriority(str, Enum):
    p0_critical = "p0_critical"
    p1_high = "p1_high"
    p2_medium = "p2_medium"
    p3_low = "p3_low"

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    blocked = "blocked"
    completed = "completed"

class EnergyLevel(str, Enum):
    deep_work = "deep_work"
    quick_win = "quick_win"
    administrative = "administrative"

class ProjectCategory(str, Enum):
    ai_systems = "ai_systems"
    research = "research"
    product = "product"
    career = "career"
    infrastructure = "infrastructure"

class ProjectStatus(str, Enum):
    active = "active"
    planned = "planned"
    completed = "completed"
    blocked = "blocked"
    maintenance = "maintenance"

class ProjectHealth(str, Enum):
    green = "green"
    yellow = "yellow"
    red = "red"

class IdeaCategory(str, Enum):
    software = "software"
    research = "research"
    venture = "venture"
    content = "content"
    personal = "personal"

class IdeaStatus(str, Enum):
    captured = "captured"
    explored = "explored"
    validated = "validated"
    planned = "planned"
    executing = "executing"
    completed = "completed"
    abandoned = "abandoned"

class IdeaPriority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class ExperimentStatus(str, Enum):
    hypothesis = "hypothesis"
    design = "design"
    running = "running"
    analyzing = "analyzing"
    concluded = "concluded"
    aborted = "aborted"

class DecisionStatus(str, Enum):
    pending_review = "pending_review"
    reviewed = "reviewed"
    superseded = "superseded"

class ResearchStatus(str, Enum):
    exploring = "exploring"
    synthesizing = "synthesizing"
    concluded = "concluded"
    dormant = "dormant"

class LearningType(str, Enum):
    book = "book"
    course = "course"
    paper = "paper"
    tutorial = "tutorial"
    topic = "topic"

class LearningStatus(str, Enum):
    queued = "queued"
    active = "active"
    paused = "paused"
    completed = "completed"

class OpportunityCategory(str, Enum):
    technology = "technology"
    career = "career"
    business = "business"
    entrepreneurship = "entrepreneurship"
    education = "education"
    investment = "investment"
    consulting = "consulting"
    partnerships = "partnerships"
    emerging_markets = "emerging_markets"

class OpportunityStatus(str, Enum):
    evaluating = "evaluating"
    pursuing = "pursuing"
    watching = "watching"
    archived = "archived"

class RelationType(str, Enum):
    leads_to = "leads_to"
    validates = "validates"
    informs = "informs"
    implements = "implements"
    spawns = "spawns"
    depends_on = "depends_on"
    references = "references"

# --- SCHEMAS ---

# 1. Tasks
class TaskBase(BaseModel):
    title: str
    project_id: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.p2_medium
    deadline: Optional[str] = None
    scheduled_date: Optional[str] = None
    blocker_reason: Optional[str] = None
    energy_level: EnergyLevel = EnergyLevel.deep_work
    tags: List[str] = Field(default_factory=list)

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

# 2. Projects
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = ""
    category: ProjectCategory = ProjectCategory.ai_systems
    status: ProjectStatus = ProjectStatus.active
    health: ProjectHealth = ProjectHealth.green
    progress_pct: int = Field(default=0, ge=0, le=100)
    next_actions: List[str] = Field(default_factory=list)
    target_date: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ProjectCategory] = None
    status: Optional[ProjectStatus] = None
    health: Optional[ProjectHealth] = None
    progress_pct: Optional[int] = Field(default=None, ge=0, le=100)
    next_actions: Optional[List[str]] = None
    target_date: Optional[str] = None

class Project(ProjectBase):
    id: str
    created_at: str
    updated_at: str

# 3. Ideas
class IdeaBase(BaseModel):
    title: str
    description: Optional[str] = ""
    category: IdeaCategory = IdeaCategory.software
    origin: Optional[str] = ""
    status: IdeaStatus = IdeaStatus.captured
    priority: IdeaPriority = IdeaPriority.medium
    next_action: Optional[str] = ""
    related_project_id: Optional[str] = None

class IdeaCreate(IdeaBase):
    pass

class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[IdeaCategory] = None
    origin: Optional[str] = None
    status: Optional[IdeaStatus] = None
    priority: Optional[IdeaPriority] = None
    next_action: Optional[str] = None
    related_project_id: Optional[str] = None

class Idea(IdeaBase):
    id: str
    created_at: str
    updated_at: str
    status_changed_at: str

# 4. Experiments
class ExperimentBase(BaseModel):
    idea_id: Optional[str] = None
    project_id: Optional[str] = None
    title: str
    hypothesis: str
    objective: str
    assumptions: List[str] = Field(default_factory=list)
    experiment_design: str
    expected_result: str
    actual_result: Optional[str] = ""
    evidence: Optional[str] = ""
    conclusion: Optional[str] = ""
    next_step: Optional[str] = ""
    status: ExperimentStatus = ExperimentStatus.hypothesis

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentUpdate(BaseModel):
    idea_id: Optional[str] = None
    project_id: Optional[str] = None
    title: Optional[str] = None
    hypothesis: Optional[str] = None
    objective: Optional[str] = None
    assumptions: Optional[List[str]] = None
    experiment_design: Optional[str] = None
    expected_result: Optional[str] = None
    actual_result: Optional[str] = None
    evidence: Optional[str] = None
    conclusion: Optional[str] = None
    next_step: Optional[str] = None
    status: Optional[ExperimentStatus] = None

class Experiment(ExperimentBase):
    id: str
    created_at: str
    updated_at: str

# 5. Decisions
class DecisionAlternative(BaseModel):
    option: str
    pros: str = ""
    cons: str = ""

class DecisionBase(BaseModel):
    title: str
    date: str
    context: str
    alternatives_considered: List[DecisionAlternative] = Field(default_factory=list)
    assumptions: str
    evidence: str
    expected_outcome: str
    actual_outcome: Optional[str] = ""
    confidence_level: int = Field(default=75, ge=1, le=100)
    lessons_learned: Optional[str] = ""
    status: DecisionStatus = DecisionStatus.pending_review
    review_date: Optional[str] = None

class DecisionCreate(DecisionBase):
    pass

class DecisionUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    context: Optional[str] = None
    alternatives_considered: Optional[List[DecisionAlternative]] = None
    assumptions: Optional[str] = None
    evidence: Optional[str] = None
    expected_outcome: Optional[str] = None
    actual_outcome: Optional[str] = None
    confidence_level: Optional[int] = Field(default=None, ge=1, le=100)
    lessons_learned: Optional[str] = None
    status: Optional[DecisionStatus] = None
    review_date: Optional[str] = None

class Decision(DecisionBase):
    id: str
    created_at: str
    updated_at: str

# 6. Research Entries
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
    findings: List[ResearchFinding] = Field(default_factory=list)
    sources: List[ResearchSource] = Field(default_factory=list)
    conclusions: Optional[str] = ""
    unresolved_questions: List[str] = Field(default_factory=list)
    related_project_id: Optional[str] = None

class ResearchEntryCreate(ResearchEntryBase):
    pass

class ResearchEntryUpdate(BaseModel):
    research_question: Optional[str] = None
    topic: Optional[str] = None
    status: Optional[ResearchStatus] = None
    investigations: Optional[str] = None
    findings: Optional[List[ResearchFinding]] = None
    sources: Optional[List[ResearchSource]] = None
    conclusions: Optional[str] = None
    unresolved_questions: Optional[List[str]] = None
    related_project_id: Optional[str] = None

class ResearchEntry(ResearchEntryBase):
    id: str
    created_at: str
    updated_at: str

# 7. Learning Items
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
    practical_exercises: List[PracticalExercise] = Field(default_factory=list)
    key_takeaways: Optional[str] = ""

class LearningItemCreate(LearningItemBase):
    pass

class LearningItemUpdate(BaseModel):
    subject: Optional[str] = None
    title: Optional[str] = None
    type: Optional[LearningType] = None
    progress_pct: Optional[int] = Field(default=None, ge=0, le=100)
    status: Optional[LearningStatus] = None
    notes: Optional[str] = None
    practical_exercises: Optional[List[PracticalExercise]] = None
    key_takeaways: Optional[str] = None

class LearningItem(LearningItemBase):
    id: str
    created_at: str
    updated_at: str

# 8. Opportunities (Opportunity Radar)
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

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    date_discovered: Optional[str] = None
    category: Optional[OpportunityCategory] = None
    potential_upside: Optional[str] = None
    requirements: Optional[str] = None
    risks: Optional[str] = None
    status: Optional[OpportunityStatus] = None
    next_action: Optional[str] = None

class Opportunity(OpportunityBase):
    id: str
    created_at: str
    updated_at: str

# 9. Knowledge Edges
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

# 10. Knowledge Graph View Schema
class GraphNode(BaseModel):
    id: str
    label: str
    type: str
    subtitle: Optional[str] = ""
    status: Optional[str] = ""
    health: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relation: str
    notes: Optional[str] = ""

class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

# 11. Universal Search Result Schema
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
    tags: List[str] = Field(default_factory=list)
    relevance_score: float = 1.0

# 12. Situational Metrics Schema
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
