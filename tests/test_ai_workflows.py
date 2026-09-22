import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db
from app.seed_data import seed_database
from app.repository import Repository

@pytest.fixture(scope="module")
def client():
    init_db()
    seed_database()
    with TestClient(app) as c:
        yield c

def test_daily_briefing_grounding(client):
    res = client.post("/api/ai/daily-briefing")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "daily_briefing"
    content = data["content"]

    # Verify presence of strict 4-bracket grounding tags
    assert "[FACT]" in content
    assert "[AI RECOMMENDATION]" in content
    # Verify it references real numbers/projects from database
    assert "active project" in content.lower()

def test_weekly_review_grounding(client):
    res = client.post("/api/ai/weekly-review")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "weekly_review"
    content = data["content"]
    assert "[FACT]" in content

def test_project_diagnostic_audit(client):
    projects = Repository.get_projects()
    assert len(projects) > 0
    p = projects[0]

    res = client.post(f"/api/ai/analyze-project/{p.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "project_analysis"
    content = data["content"]
    assert p.title in content
    assert "[FACT]" in content

def test_idea_stress_test(client):
    ideas = Repository.get_ideas()
    assert len(ideas) > 0
    idea = ideas[0]

    res = client.post(f"/api/ai/analyze-idea/{idea.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "idea_analysis"
    content = data["content"]
    assert idea.title in content
    assert "[ASSUMPTION]" in content or "[AI RECOMMENDATION]" in content

def test_decision_audit(client):
    decisions = Repository.get_decisions()
    assert len(decisions) > 0
    dec = decisions[0]

    res = client.post(f"/api/ai/review-decision/{dec.id}")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "decision_review"
    content = data["content"]
    assert dec.title in content
    assert str(dec.confidence_level) in content
