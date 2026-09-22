from app.database import init_db
from app.repository import Repository
from app.models import (
    TaskCreate, TaskStatus, TaskPriority, EnergyLevel,
    ProjectCreate, ProjectStatus, ProjectHealth, ProjectCategory,
    IdeaCreate, IdeaStatus, IdeaPriority, IdeaCategory,
    ExperimentCreate, ExperimentStatus,
    DecisionCreate, DecisionStatus, DecisionAlternative,
    ResearchEntryCreate, ResearchStatus, ResearchFinding, ResearchSource,
    LearningItemCreate, LearningStatus, LearningType, PracticalExercise,
    OpportunityCreate, OpportunityStatus, OpportunityCategory,
    KnowledgeEdgeCreate, RelationType
)

def seed_database():
    init_db()

    # Check if already seeded
    if len(Repository.get_projects()) > 0:
        print("Database already contains data, skipping seed.")
        return

    print("Populating Command Center with realistic domain data...")

    # --- 1. PROJECTS ---
    p1 = Repository.create_project(ProjectCreate(
        title="Nexus Sovereign AI Agent Architecture",
        description="High-performance, event-driven agentic framework utilizing local LLMs, strict schema grounding, and reproducible state machine transitions.",
        category=ProjectCategory.ai_systems,
        status=ProjectStatus.active,
        health=ProjectHealth.green,
        progress_pct=78,
        next_actions=[
            "Finalize zero-copy IPC serialization between orchestrator and subagents",
            "Benchmark token generation latency under concurrent subagent contention",
            "Write RFC on deterministic agent retry heuristics"
        ],
        target_date="2026-10-15"
    ))

    p2 = Repository.create_project(ProjectCreate(
        title="Autonomous Algorithmic Alpha Engine",
        description="High-frequency market microstructure analyzer and statistical arbitrage framework processing order book imbalance metrics.",
        category=ProjectCategory.product,
        status=ProjectStatus.active,
        health=ProjectHealth.yellow,
        progress_pct=45,
        next_actions=[
            "Resolve slippage calculation discrepancy in backtesting engine",
            "Incorporate order-flow toxicity (VPIN) indicator into live risk gate"
        ],
        target_date="2026-11-01"
    ))

    p3 = Repository.create_project(ProjectCreate(
        title="Edge-Compute Vision Pipeline for Jetson Orin",
        description="Ultra-low latency object detection and multi-camera spatial tracking pipeline running on constrained embedded edge hardware.",
        category=ProjectCategory.infrastructure,
        status=ProjectStatus.blocked,
        health=ProjectHealth.red,
        progress_pct=25,
        next_actions=[
            "Resolve CUDA 12.8 driver compatibility mismatch on Jetpack 6.2 OS",
            "Downgrade TensorRT runtime or apply vendor kernel patch"
        ],
        target_date="2026-10-30"
    ))

    p4 = Repository.create_project(ProjectCreate(
        title="Distributed Knowledge Graph & Memory Mesh",
        description="Persistent biographical and domain memory layer connecting relational metadata, semantic vectors, and hierarchical event logs.",
        category=ProjectCategory.research,
        status=ProjectStatus.completed,
        health=ProjectHealth.green,
        progress_pct=100,
        next_actions=[
            "Publish technical report and open-source GitHub release"
        ],
        target_date="2026-09-01"
    ))

    # --- 2. IDEAS ---
    i1 = Repository.create_idea(IdeaCreate(
        title="Adaptive Speculative Decoding for Edge Silicon",
        description="Dynamically adjust draft model length based on entropy of target model logits to maintain >2.8x speedup on local hardware.",
        category=IdeaCategory.research,
        origin="Observing speculative decoding throughput collapse on complex code generation tasks",
        status=IdeaStatus.executing,
        priority=IdeaPriority.high,
        next_action="Run empirical benchmark against standard LLaMA-3.2-3B draft model",
        related_project_id=p1.id
    ))

    i2 = Repository.create_idea(IdeaCreate(
        title="Multi-Agent Consensus Layer via Lamport Timestamps",
        description="Enforce causal consistency across autonomous subagents working on concurrent git branches without requiring a centralized coordinator.",
        category=IdeaCategory.software,
        origin="Encountered merge conflicts during multi-agent refactoring simulations",
        status=IdeaStatus.validated,
        priority=IdeaPriority.high,
        next_action="Draft formal state machine specification and mathematical proof of safety",
        related_project_id=p1.id
    ))

    i3 = Repository.create_idea(IdeaCreate(
        title="Autonomous Cloud FinOps Sentinel for GPU Clusters",
        description="Background agent that automatically migrates spot instances, terminates idle inference endpoints, and negotiates reserved pricing.",
        category=IdeaCategory.venture,
        origin="Noticed $1,400 monthly cloud waste on idle dev endpoints",
        status=IdeaStatus.planned,
        priority=IdeaPriority.medium,
        next_action="Interview 5 startup founders on their monthly cloud GPU burn",
        related_project_id=None
    ))

    i4 = Repository.create_idea(IdeaCreate(
        title="Neural Sound Synthesis via Differentiable DSP",
        description="Real-time guitar synthesizer using physical modeling combined with low-latency neural residual networks.",
        category=IdeaCategory.personal,
        origin="Jamming with analog synthesizer setup on weekend",
        status=IdeaStatus.explored,
        priority=IdeaPriority.low,
        next_action="Read recent DAFx 2025 conference proceedings on neural audio",
        related_project_id=None
    ))

    i5 = Repository.create_idea(IdeaCreate(
        title="Decentralized Peer-to-Peer Training Pool",
        description="Crowdsourced gradient descent across home consumer gaming GPUs over consumer broadband.",
        category=IdeaCategory.software,
        origin="Late-night tech discussion on bandwidth constraints",
        status=IdeaStatus.abandoned,
        priority=IdeaPriority.low,
        next_action="Abandoned: Bandwidth latency under AllReduce makes parameter sync mathematically unviable without 100Gbps links",
        related_project_id=None
    ))

    # --- 3. EXPERIMENTS ---
    e1 = Repository.create_experiment(ExperimentCreate(
        idea_id=i1.id,
        project_id=p1.id,
        title="Speculative Decoding Acceptance Rate on Apple M-Series",
        hypothesis="Dynamic draft token length (k=3 to k=7 based on Shannon entropy of top logits) increases token generation speed by at least 2.2x over greedy decoding with zero perplexity degradation.",
        objective="Quantify tokens-per-second throughput and acceptance ratios on Metal Performance Shaders (MPS).",
        assumptions=[
            "Draft model fits in unified memory alongside target 70B model",
            "Entropy threshold calculation overhead is sub-1 millisecond"
        ],
        experiment_design="Test harness with 50 coding problems from HumanEval. Compare greedy baseline vs fixed k=5 speculative vs adaptive entropy-guided speculative decoding.",
        expected_result="Throughput improves from 14 tokens/sec to >32 tokens/sec on Apple M3 Max.",
        actual_result="Achieved 34.2 tokens/sec on Python code completion. Acceptance rate maintained at 76.4% across 10,000 generated tokens.",
        evidence="Benchmark run logs archived in `/experiments/spec_decode_results_v2.json`. Peak GPU memory consumption: 42.1 GB.",
        conclusion="Hypothesis confirmed. Adaptive entropy gating outperforms static draft lengths by 18% on high-entropy branching code.",
        next_step="Integrate entropy gating heuristic into Nexus sovereign agent inference loop.",
        status=ExperimentStatus.concluded
    ))

    e2 = Repository.create_experiment(ExperimentCreate(
        idea_id=i2.id,
        project_id=p1.id,
        title="SQLite WAL Mode Concurrent Write Stress Test for 30 Subagents",
        hypothesis="Using WAL mode with PRAGMA busy_timeout=5000ms can sustain 50 concurrent writes per second without SQLITE_BUSY exceptions.",
        objective="Verify SQLite viability as single-node personal command center and agent event ledger.",
        assumptions=["NVMe SSD provides adequate IOPS for WAL flushes"],
        experiment_design="Spawn 30 concurrent asyncio workers firing 500 write transactions into SQLite simultaneously.",
        expected_result="Zero unhandled database lock errors; p99 write latency under 12ms.",
        actual_result="Completed 15,000 transactions. Zero SQLITE_BUSY exceptions. p99 write latency was 4.2ms.",
        evidence="Stress test harness completed in 3.12 seconds total.",
        conclusion="SQLite in WAL mode exceeds throughput requirements for single-operator command center by 20x.",
        next_step="Proceed with SQLite without adding complex PostgreSQL or Redis infrastructure.",
        status=ExperimentStatus.concluded
    ))

    e3 = Repository.create_experiment(ExperimentCreate(
        idea_id=None,
        project_id=p3.id,
        title="TensorRT Int8 Quantization Precision vs FP16 on Jetson Orin",
        hypothesis="INT8 PTQ calibration on YOLOv10 reduces inference latency below 6ms while retaining mAP50 > 92%.",
        objective="Validate frame rate target of 60 FPS on 4 concurrent camera streams.",
        assumptions=["Calibration dataset accurately represents night-time low-light edge cases"],
        experiment_design="Run TensorRT int8 calibrator with 1,000 synthetic driving scenes.",
        expected_result="Latency 5.4ms per frame, mAP50 degradation < 1.5%.",
        actual_result="",
        evidence="",
        conclusion="",
        next_step="Blocked on CUDA 12.8 driver kernel installation.",
        status=ExperimentStatus.running
    ))

    # --- 4. DECISIONS ---
    d1 = Repository.create_decision(DecisionCreate(
        title="Adopt FastAPI + SQLite WAL over PostgreSQL for Local-First Command Center",
        date="2026-08-20",
        context="Designing the storage architecture for Personal Command Center. Needed zero operational overhead, portable single-file backups, and instant boot without background daemon dependencies.",
        alternatives_considered=[
            DecisionAlternative(option="PostgreSQL + Docker", pros="Enterprise concurrency, rich ecosystem", cons="Requires background daemon, 200MB+ RAM footprint, setup friction"),
            DecisionAlternative(option="SQLite with WAL mode", pros="Zero daemon, single portable file, sub-millisecond local reads, embedded in Python", cons="Single-writer limitation (mitigated by WAL)"),
            DecisionAlternative(option="DuckDB", pros="Incredible analytical columnar aggregation", cons="Less suited for high-frequency row-level transactional mutations")
        ],
        assumptions="The command center is primarily single-operator with occasional parallel background subagent writes; write concurrency will not exceed 100 tx/sec.",
        evidence="Empirical stress test confirmed 15,000 concurrent writes completed in 3.1s with zero lock collisions and 4.2ms p99.",
        expected_outcome="Instant sub-10ms dashboard loads, zero maintenance, flawless cross-machine portability.",
        actual_outcome="Application boots in 35ms. Database query latency averages 0.8ms. Backups are effortless single-file copies.",
        confidence_level=95,
        lessons_learned="Defaulting to PostgreSQL for single-user apps is architectural over-engineering. SQLite with WAL mode is exceptionally powerful.",
        status=DecisionStatus.reviewed,
        review_date="2026-09-20"
    ))

    d2 = Repository.create_decision(DecisionCreate(
        title="Pivot Agent Coordination from Monolithic Loop to Explicit State Machine",
        date="2026-09-05",
        context="Autonomous agents in the Nexus project were suffering from infinite recovery loops and indeterminate failures when encountering compiler errors.",
        alternatives_considered=[
            DecisionAlternative(option="Prompt-based self-reflection", pros="Easy to implement", cons="Nondeterministic, gets stuck in repetitive loops"),
            DecisionAlternative(option="Strict Finite State Machine with explicit transitions", pros="Deterministic, formal error states, inspectable audit trail", cons="More boilerplate code upfront")
        ],
        assumptions="State transitions can be formally cataloged into 7 discrete lifecycle states.",
        evidence="Testing showed 100% loop termination and zero hallucinated states after enforcing FSM constraints.",
        expected_outcome="Elimination of rogue subagent loops and 100% verifiable transition logging.",
        actual_outcome="Agent failure rate dropped from 28% to 2.1%. Diagnostic visibility dramatically improved.",
        confidence_level=90,
        lessons_learned="Never rely on LLM prompts to govern lifecycle safety. Enforce safety at the architectural state-machine layer.",
        status=DecisionStatus.reviewed,
        review_date="2026-09-18"
    ))

    d3 = Repository.create_decision(DecisionCreate(
        title="Select TensorRT over ONNX Runtime for Edge Vision Deployment",
        date="2026-09-15",
        context="Selecting inference engine for Jetson Orin deployment to maximize frame rates and memory bandwidth efficiency.",
        alternatives_considered=[
            DecisionAlternative(option="Nvidia TensorRT", pros="Deepest hardware optimization for Jetson DLA/Tensor Cores", cons="Rigid driver/CUDA version coupling"),
            DecisionAlternative(option="ONNX Runtime GPU", pros="Flexible, broader model support", cons="15-20% higher latency on Jetson hardware")
        ],
        assumptions="Jetpack 6.2 OS would support current TensorRT release out of the box.",
        evidence="Early micro-benchmarks showed 1.8x frame rate advantage for TensorRT.",
        expected_outcome="60 FPS sustained multi-camera tracking.",
        actual_outcome="Driver incompatibility on Jetpack 6.2 currently blocking deployment. Working on patch.",
        confidence_level=70,
        lessons_learned="Aggressive hardware optimization comes with severe dependency fragility. Always verify driver compatibility before locking architecture.",
        status=DecisionStatus.pending_review,
        review_date="2026-10-10"
    ))

    # --- 5. RESEARCH ENTRIES ---
    r1 = Repository.create_research_entry(ResearchEntryCreate(
        research_question="Can speculative decoding achieve >2.5x throughput on Apple Silicon Unified Memory without accuracy degradation?",
        topic="Efficient LLM Inference",
        status=ResearchStatus.concluded,
        investigations="Investigated token verification mechanics in autoregressive transformers. Benchmarked KV-cache sharing strategies between draft model (Llama-3.2-1B) and target model (Llama-3.1-8B). Tested impact of Shannon entropy gating on acceptance rates across diverse text distributions.",
        findings=[
            ResearchFinding(claim="Speculative acceptance rates on Python code exceed 75% due to structured syntax repetition", evidence="HumanEval 50-problem benchmark", confidence="very_high"),
            ResearchFinding(claim="Entropy-guided draft length reduces wasted verification compute by 22%", evidence="Comparative execution traces on MPS", confidence="high"),
            ResearchFinding(claim="Unified memory bus bandwidth (400 GB/s) prevents memory stalls during simultaneous weights access", evidence="Apple Instruments Metal System Trace", confidence="high")
        ],
        sources=[
            ResearchSource(title="Fast Inference from Transformers via Speculative Decoding", url_or_citation="Leviathan et al., ICML 2023", type="paper"),
            ResearchSource(title="Accelerating Large Language Model Decoding with Speculative Sampling", url_or_citation="Chen et al., NeurIPS 2023", type="paper"),
            ResearchSource(title="Apple Metal Performance Shaders Graph Documentation", url_or_citation="developer.apple.com/metal", type="documentation")
        ],
        conclusions="Speculative decoding is highly effective on Apple Silicon unified memory architectures. With adaptive entropy gating, real-world coding throughput reaches 34 tokens/sec on 70B parameter models.",
        unresolved_questions=[
            "How does multi-candidate speculative tree decoding (e.g. Medusa/Eagle) compare in memory overhead?",
            "Can we train an ultra-compact 150M parameter draft model specifically fine-tuned for verification acceptance?"
        ],
        related_project_id=p1.id
    ))

    r2 = Repository.create_research_entry(ResearchEntryCreate(
        research_question="What consensus protocol offers optimal latency and partition tolerance for local multi-agent fleets?",
        topic="Distributed Agent Systems",
        status=ResearchStatus.exploring,
        investigations="Evaluating Raft vs. Conflict-Free Replicated Data Types (CRDTs) vs. Vector Clock causality for subagents operating across local filesystems and git branches.",
        findings=[
            ResearchFinding(claim="Raft leader election introduces unnecessary coordination bottlenecks for peer agents with disjoint workspaces", evidence="Simulation with 10 agents", confidence="high"),
            ResearchFinding(claim="Operation-based CRDTs allow seamless conflict-free merge of structured JSON documents", evidence="Automerge integration prototype", confidence="medium")
        ],
        sources=[
            ResearchSource(title="Conflict-free Replicated Data Types", url_or_citation="Shapiro et al., SSS 2011", type="paper"),
            ResearchSource(title="Designing Data-Intensive Applications, Chapter 5-9", url_or_citation="Kleppmann, O'Reilly 2017", type="book")
        ],
        conclusions="CRDT-based state reconciliation is superior to quorum consensus for autonomous coding agents with localized task scopes.",
        unresolved_questions=[
            "Handling semantic merge conflicts when two agents modify interdependent Python function signatures?"
        ],
        related_project_id=p1.id
    ))

    # --- 6. LEARNING ITEMS ---
    l1 = Repository.create_learning_item(LearningItemCreate(
        subject="Systems & GPU Engineering",
        title="CUDA C++ Programming & Tensor Core Acceleration",
        type=LearningType.course,
        progress_pct=72,
        status=LearningStatus.active,
        notes="Mastering memory hierarchy: Global memory coalescing, shared memory bank conflicts, warp shuffle intrinsics, and WMMA (Warp Matrix Multiply and Accumulate) instructions.",
        practical_exercises=[
            PracticalExercise(title="Naive vs Coalesced Matrix Multiplication Kernel", completed=True),
            PracticalExercise(title="Shared Memory Tiled GEMM with Bank Conflict Avoidance", completed=True),
            PracticalExercise(title="Warp Shuffle Reduction Primitive", completed=True),
            PracticalExercise(title="Custom FlashAttention-2 Triton / CUDA Kernel", completed=False)
        ],
        key_takeaways="Memory bandwidth is almost always the true bottleneck in modern neural workloads. Minimizing round-trips to HBM via shared memory tiling yields 10x speedups."
    ))

    l2 = Repository.create_learning_item(LearningItemCreate(
        subject="Distributed Systems",
        title="Designing Data-Intensive Applications (2nd Readthrough)",
        type=LearningType.book,
        progress_pct=90,
        status=LearningStatus.active,
        notes="Deep dive into Chapter 7 (Transactions, Serializability, SSI) and Chapter 8-9 (Consistency and Consensus, Total Order Broadcast).",
        practical_exercises=[
            PracticalExercise(title="Implement Write-Ahead Log (WAL) with segment rotation in Python", completed=True),
            PracticalExercise(title="Build a minimal 3-node Raft consensus cluster with heartbeat elections", completed=True),
            PracticalExercise(title="Benchmark Two-Phase Locking vs Snapshot Isolation under heavy write skew", completed=False)
        ],
        key_takeaways="Strict serializability is rarely needed in practice; snapshot isolation combined with conflict-free domain designs avoids distributed locking overheads."
    ))

    l3 = Repository.create_learning_item(LearningItemCreate(
        subject="Financial Engineering",
        title="Algorithmic Trading & High-Frequency Order Flow Analysis",
        type=LearningType.tutorial,
        progress_pct=40,
        status=LearningStatus.active,
        notes="Focusing on limit order book dynamics, micro-price calculation, tick-level statistical modeling, and adverse selection mitigation.",
        practical_exercises=[
            PracticalExercise(title="Parse binary L3 order book market data feed", completed=True),
            PracticalExercise(title="Calculate Volume-Synchronized Probability of Toxicity (VPIN)", completed=False)
        ],
        key_takeaways="Microstructure signals decay in milliseconds. Latency jitter is more destructive than average latency."
    ))

    # --- 7. OPPORTUNITIES ---
    o1 = Repository.create_opportunity(OpportunityCreate(
        title="Technical Advisory Role at Edge AI Silicon Startup",
        description="Invited to advise early-stage startup developing dedicated NPU hardware accelerators for LLM speculative decoding and local agent execution.",
        source="Direct invitation from founder via alumni network",
        date_discovered="2026-09-10",
        category=OpportunityCategory.career,
        potential_upside="Equity advisory grant (0.25% - 0.50%), early access to next-gen silicon test boards, influence on hardware architecture.",
        requirements="5 hours per month strategic architecture review, evaluation of compiler toolchains.",
        risks="Startup hardware execution risk; potential time distraction if boundaries not held firmly.",
        status=OpportunityStatus.pursuing,
        next_action="Schedule 45-minute technical deep-dive call with CTO on Thursday at 16:00."
    ))

    o2 = Repository.create_opportunity(OpportunityCreate(
        title="Enterprise License for Agentic DevOps Orchestrator",
        description="Series B fintech startup interested in licensing our sovereign agent orchestration architecture for automated internal compliance audits.",
        source="Inbound inquiry following technical blog post on agent state machines",
        date_discovered="2026-09-14",
        category=OpportunityCategory.business,
        potential_upside="Initial $120,000 annual recurring contract plus custom integration fee.",
        requirements="SOC2 compliance readiness, on-prem deployment guide, SLAs for agent safety.",
        risks="Customer support drag; requirement for enterprise SSO and audit logging before closing.",
        status=OpportunityStatus.evaluating,
        next_action="Send redacted architectural overview and run live sandboxed demo next week."
    ))

    o3 = Repository.create_opportunity(OpportunityCreate(
        title="Angel Investment Syndicate: Local AI Inference Appliances",
        description="Participate in seed financing round for developer-first desktop compute cluster equipped with 192GB unified RAM.",
        source="AngelList venture syndicate lead",
        date_discovered="2026-08-28",
        category=OpportunityCategory.investment,
        potential_upside="5x-10x upside if local private AI hardware captures sovereign developer market.",
        requirements="$15,000 minimum investment check size.",
        risks="Capital lockup for 5-7 years; fierce competition from Apple and Nvidia consumer chips.",
        status=OpportunityStatus.watching,
        next_action="Review Q3 unit economics and manufacturing BOM breakdown before committing capital."
    ))

    # --- 8. TASKS ---
    Repository.create_task(TaskCreate(
        title="Resolve Jetson Orin CUDA 12.8 driver kernel incompatibility",
        project_id=p3.id,
        status=TaskStatus.blocked,
        priority=TaskPriority.p0_critical,
        deadline="2026-09-24T18:00:00+00:00",
        scheduled_date="2026-09-23",
        blocker_reason="Awaiting patched Jetpack 6.2 kernel header package from vendor forum",
        energy_level=EnergyLevel.deep_work,
        tags=["edge", "cuda", "jetson", "blocker"]
    ))

    Repository.create_task(TaskCreate(
        title="Benchmark speculative decoding token acceptance rates on Python AST nodes",
        project_id=p1.id,
        status=TaskStatus.in_progress,
        priority=TaskPriority.p1_high,
        deadline="2026-09-25T14:00:00+00:00",
        scheduled_date="2026-09-23",
        energy_level=EnergyLevel.deep_work,
        tags=["inference", "benchmarks", "mps"]
    ))

    Repository.create_task(TaskCreate(
        title="Prepare technical advisory review slides for Edge AI Silicon call",
        project_id=None,
        status=TaskStatus.todo,
        priority=TaskPriority.p1_high,
        deadline="2026-09-24T12:00:00+00:00",
        scheduled_date="2026-09-24",
        energy_level=EnergyLevel.deep_work,
        tags=["advisory", "career", "hardware"]
    ))

    Repository.create_task(TaskCreate(
        title="Implement order-flow toxicity (VPIN) metric in alpha backtesting harness",
        project_id=p2.id,
        status=TaskStatus.todo,
        priority=TaskPriority.p2_medium,
        deadline="2026-09-28T17:00:00+00:00",
        scheduled_date="2026-09-25",
        energy_level=EnergyLevel.deep_work,
        tags=["trading", "quant", "backtesting"]
    ))

    Repository.create_task(TaskCreate(
        title="Complete CUDA practical exercise 4: Custom FlashAttention-2 Triton kernel",
        project_id=None,
        status=TaskStatus.todo,
        priority=TaskPriority.p2_medium,
        deadline="2026-09-27T20:00:00+00:00",
        scheduled_date="2026-09-26",
        energy_level=EnergyLevel.deep_work,
        tags=["learning", "cuda", "triton"]
    ))

    Repository.create_task(TaskCreate(
        title="Audit Q3 cloud server expenses and terminate stale dev GPU instances",
        project_id=None,
        status=TaskStatus.completed,
        priority=TaskPriority.p3_low,
        deadline="2026-09-21T18:00:00+00:00",
        scheduled_date="2026-09-21",
        energy_level=EnergyLevel.quick_win,
        tags=["finops", "admin"]
    ))

    # --- 9. KNOWLEDGE EDGES ---
    # Idea -> Research -> Experiment -> Decision -> Project -> Outcome
    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="idea",
        source_id=i1.id,
        target_type="research",
        target_id=r1.id,
        relation_type=RelationType.informs,
        notes="Speculative decoding idea spurred structured research dossier"
    ))

    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="research",
        source_id=r1.id,
        target_type="experiment",
        target_id=e1.id,
        relation_type=RelationType.validates,
        notes="Research findings validated empirically via M-Series benchmark"
    ))

    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="experiment",
        source_id=e1.id,
        target_type="decision",
        target_id=d1.id,
        relation_type=RelationType.informs,
        notes="Benchmark metrics informed low-overhead architecture decisions"
    ))

    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="decision",
        source_id=d1.id,
        target_type="project",
        target_id=p1.id,
        relation_type=RelationType.implements,
        notes="Architectural decision implemented within sovereign agent framework"
    ))

    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="project",
        source_id=p1.id,
        target_type="opportunity",
        target_id=o1.id,
        relation_type=RelationType.spawns,
        notes="Nexus agent project reputation spawned Silicon advisory opportunity"
    ))

    Repository.create_edge(KnowledgeEdgeCreate(
        source_type="learning",
        source_id=l1.id,
        target_type="project",
        target_id=p3.id,
        relation_type=RelationType.informs,
        notes="CUDA engineering curriculum directly feeds into edge vision optimization"
    ))

    print("Sample data successfully populated.")

if __name__ == "__main__":
    seed_database()
