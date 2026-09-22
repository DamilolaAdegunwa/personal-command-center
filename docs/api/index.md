# API Reference Overview & Standards

This directory contains the formal API documentation for the **Personal Command Center** backend.

---

## 1. Protocol & Transport Standards

- **Base URL:** `http://127.0.0.1:8000`
- **Data Format:** JSON (`application/json; charset=utf-8`)
- **Protocol:** HTTP/1.1 over TCP loopback
- **CORS Policy:** Permissive for localhost development:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
- **Authentication:** None required. The system is designed for local single-user sovereignty.

---

## 2. Standard HTTP Response Status Codes

| Code | Status | Meaning in Personal Command Center |
|---|---|---|
| `200` | OK | Request succeeded. Returns requested entity or list. |
| `404` | Not Found | Requested entity ID does not exist in SQLite database. |
| `422` | Unprocessable Entity | Pydantic schema validation failure (e.g., missing required fields, invalid enum value, out-of-range percentage). |
| `500` | Internal Server Error | Unhandled server error (e.g., SQLite file lock, disk full). |

---

## 3. Standard Error Envelope

When a client provides invalid input or requests a missing entity, FastAPI returns standard error structures:

### 404 Not Found Example
```json
{
  "detail": "Project not found"
}
```

### 422 Validation Error Example
```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "category"],
      "msg": "Input should be 'ai_systems', 'research', 'product', 'career' or 'infrastructure'",
      "input": "invalid_category"
    }
  ]
}
```

---

## 4. API Documentation Modules

- **[Endpoints Reference](endpoints.md):** Complete catalog of all endpoints grouped by domain resource.
- **[Data Schemas](schemas.md):** Pydantic schema models, field typing, defaults, and validation constraints.
