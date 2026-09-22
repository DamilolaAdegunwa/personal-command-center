import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed_data import seed_database

@pytest.fixture(scope="module")
def client():
    init_db()
    seed_database()
    with TestClient(app) as c:
        yield c

def test_healthcheck(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "operational"
    assert "version" in data

def test_today_dashboard(client):
    res = client.get("/api/today")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert "critical_p0" in data
    assert "blocked_items" in data
    assert "active_projects" in data
    assert data["summary"]["active_projects_count"] >= 1

def test_projects_crud(client):
    # 1. Create
    new_proj = {
        "title": "Quantum Memory Shm Engine",
        "description": "Ultra low latency inter-process communication",
        "category": "ai_systems",
        "status": "active",
        "health": "green",
        "progress_pct": 10,
        "next_actions": ["Write POSIX shm binding"],
        "target_date": "2026-11-15"
    }
    create_res = client.post("/api/projects", json=new_proj)
    assert create_res.status_code == 200
    p_id = create_res.json()["id"]

    # 2. Get
    get_res = client.get(f"/api/projects/{p_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == new_proj["title"]

    # 3. Update
    up_res = client.put(f"/api/projects/{p_id}", json={"progress_pct": 35, "health": "yellow"})
    assert up_res.status_code == 200
    assert up_res.json()["progress_pct"] == 35
    assert up_res.json()["health"] == "yellow"

    # 4. Delete
    del_res = client.delete(f"/api/projects/{p_id}")
    assert del_res.status_code == 200
    assert client.get(f"/api/projects/{p_id}").status_code == 404

def test_ideas_lifecycle_state_machine(client):
    # Create captured idea
    new_idea = {
        "title": "Kernel-Level Attention Pruning",
        "description": "Sparsify attention matrices at GPU warp level",
        "category": "software",
        "origin": "Reading FlashAttention-3 paper",
        "status": "captured",
        "priority": "high",
        "next_action": "Profile memory bandwidth"
    }
    res = client.post("/api/ideas", json=new_idea)
    assert res.status_code == 200
    idea_id = res.json()["id"]
    assert res.json()["status"] == "captured"

    # Advance state: captured -> explored -> validated -> planned
    for target in ["explored", "validated", "planned", "executing"]:
        t_res = client.post(f"/api/ideas/{idea_id}/transition?target_status={target}")
        assert t_res.status_code == 200
        assert t_res.json()["status"] == target

    # Delete
    client.delete(f"/api/ideas/{idea_id}")

def test_experiments_workflow(client):
    new_exp = {
        "title": "Attention Head Sparsity vs Perplexity",
        "hypothesis": "Dropping 40% of non-critical attention heads reduces memory by 30% with <0.1 perplexity loss",
        "objective": "Measure latency and perplexity on Wikitext-2",
        "assumptions": ["Heads can be identified by L1 norm of activation weights"],
        "experiment_design": "Evaluate 100 test prompts with pruned attention masks",
        "expected_result": "Throughput increases by 1.4x",
        "status": "hypothesis"
    }
    res = client.post("/api/experiments", json=new_exp)
    assert res.status_code == 200
    exp_id = res.json()["id"]

    # Update with empirical evidence
    up_res = client.put(f"/api/experiments/{exp_id}", json={
        "status": "concluded",
        "actual_result": "Achieved 1.38x throughput with 0.08 perplexity degradation",
        "evidence": "Benchmark log benchmark_pruning_v1.json",
        "conclusion": "Hypothesis validated for coding and math domains"
    })
    assert up_res.status_code == 200
    assert up_res.json()["status"] == "concluded"
    assert "actual_result" in up_res.json()

    client.delete(f"/api/experiments/{exp_id}")

def test_decisions_intelligence(client):
    new_dec = {
        "title": "Migrate from REST to gRPC for Internal IPC",
        "date": "2026-09-22",
        "context": "Agent sub-processes require microsecond message passing",
        "alternatives_considered": [
            {"option": "gRPC", "pros": "Protobuf serialization, HTTP/2 streaming", "cons": "More schema overhead"},
            {"option": "REST JSON", "pros": "Simple, readable", "cons": "Text serialization overhead"}
        ],
        "assumptions": "Message volume exceeds 500 msgs/sec",
        "evidence": "Microbenchmark showed JSON serialization consumed 18% CPU",
        "expected_outcome": "p99 serialization latency under 0.2ms",
        "confidence_level": 88,
        "status": "pending_review",
        "review_date": "2026-10-22"
    }
    res = client.post("/api/decisions", json=new_dec)
    assert res.status_code == 200
    dec_id = res.json()["id"]
    assert res.json()["confidence_level"] == 88

    client.delete(f"/api/decisions/{dec_id}")

def test_research_entries(client):
    new_res = {
        "research_question": "Can FlashDecoding be extended to tree-structured token candidates?",
        "topic": "Parallel LLM Decoding",
        "status": "exploring",
        "investigations": "Examining prefix tree caching in GPU shared memory",
        "findings": [
            {"claim": "Prefix sharing reduces redundant GEMV operations by up to 55%", "evidence": "CUDA simulation", "confidence": "high"}
        ],
        "sources": [
            {"title": "Flash-Decoding for long-context generation", "url_or_citation": "Dao et al., 2023", "type": "paper"}
        ],
        "conclusions": "Feasible with custom warp reduction kernel",
        "unresolved_questions": ["Optimal tree branching factor under 32KB shared memory limits"]
    }
    res = client.post("/api/research", json=new_res)
    assert res.status_code == 200
    r_id = res.json()["id"]
    assert res.json()["findings"][0]["claim"].startswith("Prefix sharing")

    client.delete(f"/api/research/{r_id}")

def test_learning_items(client):
    new_learn = {
        "subject": "Compilers",
        "title": "LLVM Infrastructure & MLIR Dialects",
        "type": "course",
        "progress_pct": 50,
        "status": "active",
        "notes": "Understanding progressive lowering from High-Level IR to LLVM IR",
        "practical_exercises": [
            {"title": "Build a toy AST parser", "completed": True},
            {"title": "Implement constant folding pass", "completed": False}
        ],
        "key_takeaways": "MLIR simplifies multi-level domain-specific optimizations."
    }
    res = client.post("/api/learning", json=new_learn)
    assert res.status_code == 200
    l_id = res.json()["id"]
    assert res.json()["progress_pct"] == 50

    client.delete(f"/api/learning/{l_id}")

def test_opportunity_radar(client):
    new_opp = {
        "title": "Founding Engineer at Sovereign AI Labs",
        "description": "Leading development of local private inference appliances",
        "date_discovered": "2026-09-20",
        "category": "career",
        "potential_upside": "High equity package and leadership of systems team",
        "requirements": "Deep expertise in CUDA, PyTorch C++ extensions, and distributed agents",
        "risks": "Early stage venture risk",
        "status": "evaluating",
        "next_action": "Initial interview with founders"
    }
    res = client.post("/api/opportunities", json=new_opp)
    assert res.status_code == 200
    o_id = res.json()["id"]
    assert res.json()["category"] == "career"

    client.delete(f"/api/opportunities/{o_id}")

def test_universal_omni_search(client):
    res = client.get("/api/search?q=speculative")
    assert res.status_code == 200
    results = res.json()
    assert len(results) > 0
    # Every item has snippet and title
    assert all("title" in item and "snippet" in item for item in results)

def test_knowledge_graph_data(client):
    res = client.get("/api/graph")
    assert res.status_code == 200
    graph = res.json()
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) >= 5
    assert len(graph["edges"]) >= 3

def test_situational_metrics(client):
    res = client.get("/api/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert "active_projects" in metrics
    assert "ideas_captured" in metrics
    assert "project_health_breakdown" in metrics
    assert "stagnation_alerts" in metrics
