# Engineering Conventions & Code Standards

This document establishes the architectural, coding, and testing conventions enforced across the **Personal Command Center** codebase.

---

## 1. Python & Backend Conventions

### 1.1 Python Version & Type Annotations
- **Runtime:** Python 3.14+ (compatible with 3.12+).
- **Type Hints:** All function signatures must include comprehensive type annotations:
  ```python
  from typing import List, Optional, Dict, Any

  def get_tasks(
      status: Optional[str] = None,
      priority: Optional[str] = None,
      project_id: Optional[str] = None
  ) -> List[Task]:
      ...
  ```
- **Pydantic v2 Models:**
  - Ingestion models inherit from base schemas (e.g. `TaskCreate(TaskBase)`).
  - Update models declare all fields as `Optional[...] = None` to allow partial patching.
  - Percentage fields must use bounded validation: `Field(default=0, ge=0, le=100)`.

### 1.2 Separation of Concerns
- **`app/main.py` (Thin Controller):**
  - Handles routing, query parsing, and HTTP status codes.
  - Never executes direct SQL queries or complex business heuristics.
- **`app/repository.py` (Data Access):**
  - Encapsulates all SQL statements.
  - Marshals database rows into Pydantic models.
- **`app/ai_service.py`, `app/graph_service.py`, `app/search_service.py`, `app/metrics_service.py` (Domain Services):**
  - Pure business logic and computational synthesis.

### 1.3 SQL Safety & Parameterization
- **Strict Parameterization:** Dynamic SQL values must NEVER use Python string formatting (`f"..."` or `%s`). Always use parameter markers (`?`):
  ```python
  # CORRECT:
  conn.execute("SELECT * FROM tasks WHERE status = ?", (status,))

  # FORBIDDEN (SQL Injection Risk):
  # conn.execute(f"SELECT * FROM tasks WHERE status = '{status}'")
  ```
- **Connection Hygiene:** Always close connections explicitly or use context managers:
  ```python
  conn = get_connection()
  try:
      # database operations
      conn.commit()
  finally:
      conn.close()
  ```

---

## 2. Frontend Conventions

### 2.1 Vanilla ES6 & No Build Tool
- Zero external build tool dependencies (no Webpack, Vite, or npm required).
- Use native browser ES modules (`import { ... } from './api.js'`).
- Use CSS Custom Properties defined in `:root` for consistent color schemes.

### 2.2 Error Handling & User Feedback
- Network operations must be wrapped in `try ... catch`.
- Client errors must surface non-blocking notifications via `showToast(message, type)`.
- Global hotkeys must ignore keystrokes when the user is actively typing in an `<input>`, `<textarea>`, or `<select>`.

---

## 3. Testing Conventions

- **Test Framework:** `pytest` with `fastapi.testclient.TestClient`.
- **Fixtures:** Use `scope="module"` fixtures for the test client in `conftest.py` or test files:
  ```python
  @pytest.fixture(scope="module")
  def client():
      init_db()
      seed_database()
      with TestClient(app) as c:
          yield c
  ```
- **Deterministic Assertions:** Assert specific HTTP response codes, JSON keys, and grounded tags (`[FACT]`, `[AI RECOMMENDATION]`).
