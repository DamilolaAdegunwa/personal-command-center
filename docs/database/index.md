# Database & Storage Overview

This directory documents the database architecture, transactional storage engine, and persistence patterns of the **Personal Command Center**.

---

## 1. Database Technology Selection

The Personal Command Center utilizes **SQLite 3.50+** as its primary data store. SQLite was chosen for this architecture based on the following verified advantages:

- **Local Sovereignty:** Zero cloud dependencies, zero external network hops, zero SaaS subscription overhead. The user's entire life and work memory resides in a single portable file (`personal_os.db`).
- **Sub-Millisecond Query Latency:** In-process C-level access eliminates network socket roundtrips typical of client-server databases (e.g. PostgreSQL, MySQL).
- **Zero Administrative Overhead:** No separate background daemon to manage, upgrade, or monitor.
- **ACID Durability:** Full atomic transactions with crash protection.

---

## 2. Storage Architecture & WAL Mode

By default, standard SQLite uses rollback journals which lock the entire database during write transactions. Personal Command Center explicitly configures **Write-Ahead Logging (`WAL`)**:

```
+-----------------------------------------------------------------------+
|                           FILESYSTEM DIRECTORY                        |
|                                                                       |
|  +--------------------+  +--------------------+  +-----------------+  |
|  |   personal_os.db   |  | personal_os.db-wal |  |personal_os.db-shm| |
|  | (Main B-Tree Data) |  | (Write-Ahead Log)  |  | (Shared Memory) |  |
|  +--------------------+  +--------------------+  +-----------------+  |
|            ^                       ^                       ^          |
|            |                       |                       |          |
|      Base Storage             Append Writes          Reader Indices   |
+-----------------------------------------------------------------------+
```

### Architectural Benefits:
1. **Concurrency:** Multiple concurrent read operations proceed simultaneously without blocking incoming write operations.
2. **Sequential Disk I/O:** Write operations are appended sequentially to the WAL log file, significantly improving write throughput.
3. **Crash Resilience:** Changes in the WAL file are safely recovered even in the event of sudden operating system crashes or power failures.

---

## 3. Connection Management & Transactions

Database access is managed through `app.database.get_connection()`:

```python
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA busy_timeout = 5000;")
    return conn
```

- **Row Factory:** Configured to `sqlite3.Row` allowing dictionary-like column name lookups (`r["title"]`).
- **Transaction Boundaries:** Transactions are committed explicitly in `app.repository.py` using `conn.commit()`.
- **Busy Timeout:** A 5,000ms busy timeout ensures that if two operations write simultaneously, the second will block and wait rather than throwing a lock error.

---

## 4. Documentation Guides in this Section

- **[Schema Specification](schema.md):** Complete table definitions, foreign key constraints, indexes, and full ER diagram.
- **[Queries & Performance](queries-and-performance.md):** Index utilization, JSON query patterns, maintenance procedures, and backup workflows.
