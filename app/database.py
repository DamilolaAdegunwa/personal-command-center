import os
import sqlite3
import json
from pathlib import Path
from typing import Optional

DB_PATH = os.getenv("COMMAND_CENTER_DB", str(Path(__file__).parent.parent / "personal_os.db"))

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    -- 1. Tasks
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        project_id TEXT,
        status TEXT NOT NULL DEFAULT 'todo',
        priority TEXT NOT NULL DEFAULT 'p2_medium',
        deadline TEXT,
        scheduled_date TEXT,
        blocker_reason TEXT,
        energy_level TEXT DEFAULT 'deep_work',
        tags TEXT DEFAULT '[]',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        completed_at TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
    CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
    CREATE INDEX IF NOT EXISTS idx_tasks_deadline ON tasks(deadline);
    CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);

    -- 2. Projects
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL DEFAULT 'ai_systems',
        status TEXT NOT NULL DEFAULT 'active',
        health TEXT NOT NULL DEFAULT 'green',
        progress_pct INTEGER NOT NULL DEFAULT 0,
        next_actions TEXT DEFAULT '[]',
        target_date TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
    CREATE INDEX IF NOT EXISTS idx_projects_health ON projects(health);

    -- 3. Ideas
    CREATE TABLE IF NOT EXISTS ideas (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL DEFAULT 'software',
        origin TEXT,
        status TEXT NOT NULL DEFAULT 'captured',
        priority TEXT NOT NULL DEFAULT 'medium',
        next_action TEXT,
        related_project_id TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        status_changed_at TEXT NOT NULL,
        FOREIGN KEY (related_project_id) REFERENCES projects(id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
    CREATE INDEX IF NOT EXISTS idx_ideas_priority ON ideas(priority);

    -- 4. Experiments
    CREATE TABLE IF NOT EXISTS experiments (
        id TEXT PRIMARY KEY,
        idea_id TEXT,
        project_id TEXT,
        title TEXT NOT NULL,
        hypothesis TEXT NOT NULL,
        objective TEXT NOT NULL,
        assumptions TEXT DEFAULT '[]',
        experiment_design TEXT NOT NULL,
        expected_result TEXT NOT NULL,
        actual_result TEXT,
        evidence TEXT,
        conclusion TEXT,
        next_step TEXT,
        status TEXT NOT NULL DEFAULT 'hypothesis',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (idea_id) REFERENCES ideas(id) ON DELETE SET NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_experiments_status ON experiments(status);

    -- 5. Decisions
    CREATE TABLE IF NOT EXISTS decisions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        context TEXT NOT NULL,
        alternatives_considered TEXT DEFAULT '[]',
        assumptions TEXT NOT NULL,
        evidence TEXT NOT NULL,
        expected_outcome TEXT NOT NULL,
        actual_outcome TEXT,
        confidence_level INTEGER NOT NULL DEFAULT 75,
        lessons_learned TEXT,
        status TEXT NOT NULL DEFAULT 'pending_review',
        review_date TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_decisions_status ON decisions(status);
    CREATE INDEX IF NOT EXISTS idx_decisions_review_date ON decisions(review_date);

    -- 6. Research Entries
    CREATE TABLE IF NOT EXISTS research_entries (
        id TEXT PRIMARY KEY,
        research_question TEXT NOT NULL,
        topic TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'exploring',
        investigations TEXT,
        findings TEXT DEFAULT '[]',
        sources TEXT DEFAULT '[]',
        conclusions TEXT,
        unresolved_questions TEXT DEFAULT '[]',
        related_project_id TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (related_project_id) REFERENCES projects(id) ON DELETE SET NULL
    );

    CREATE INDEX IF NOT EXISTS idx_research_status ON research_entries(status);
    CREATE INDEX IF NOT EXISTS idx_research_topic ON research_entries(topic);

    -- 7. Learning Items
    CREATE TABLE IF NOT EXISTS learning_items (
        id TEXT PRIMARY KEY,
        subject TEXT NOT NULL,
        title TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'book',
        progress_pct INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'active',
        notes TEXT,
        practical_exercises TEXT DEFAULT '[]',
        key_takeaways TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_learning_status ON learning_items(status);

    -- 8. Opportunities
    CREATE TABLE IF NOT EXISTS opportunities (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        source TEXT,
        date_discovered TEXT NOT NULL,
        category TEXT NOT NULL,
        potential_upside TEXT,
        requirements TEXT,
        risks TEXT,
        status TEXT NOT NULL DEFAULT 'evaluating',
        next_action TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
    CREATE INDEX IF NOT EXISTS idx_opportunities_category ON opportunities(category);

    -- 9. Knowledge Edges
    CREATE TABLE IF NOT EXISTS knowledge_edges (
        id TEXT PRIMARY KEY,
        source_type TEXT NOT NULL,
        source_id TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_id TEXT NOT NULL,
        relation_type TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_edges_source ON knowledge_edges(source_type, source_id);
    CREATE INDEX IF NOT EXISTS idx_edges_target ON knowledge_edges(target_type, target_id);
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
