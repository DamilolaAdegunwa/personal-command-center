# Security Architecture & Threat Model

This document establishes the security model, risk profile, and data protection mechanisms of the **Personal Command Center**.

---

## 1. Security Architecture & Threat Model

The Personal Command Center is designed around the premise of **personal data sovereignty**:

```
+-------------------------------------------------------------------------+
|                         LOCAL SOVEREIGNTY ZONE                          |
|                                                                         |
|   +--------------------+     HTTP (Loopback)     +------------------+   |
|   |   User Browser     | <====================> |  FastAPI Server  |   |
|   |  (127.0.0.1:8000)  |                        |  (127.0.0.1:8000)|   |
|   +--------------------+                        +------------------+   |
|                                                           |             |
|                                                    POSIX Syscalls       |
|                                                           v             |
|                                                 +--------------------+  |
|                                                 | SQLite File Store  |  |
|                                                 | (personal_os.db)   |  |
|                                                 +--------------------+  |
+-------------------------------------------------------------------------+
                                    |
                    Outbound HTTPS (TLS 1.3) / Port 443
                        (Optional: GEMINI_API_KEY)
                                    v
                  +----------------------------------+
                  |  Google Gemini Cloud Endpoint    |
                  +----------------------------------+
```

### Core Security Boundaries:
1. **Loopback Binding Isolation:** The application binds by default to `127.0.0.1:8000`, preventing remote devices on the local area network (LAN) from accessing the API or database.
2. **Localhost Data Sovereignty:** Personal notes, commitments, ideas, and decisions are stored exclusively on the user's physical drive. No telemetry, usage analytics, or cloud synchronization occurs without user action.
3. **Additive Cloud LLM Isolation:** When Google Gemini is utilized, only task titles, project names, and decision contexts necessary for synthesis are transmitted over TLS 1.3.

---

## 2. Security Controls

### 2.1 Input Validation & Type Safety
- Every incoming HTTP request payload is strictly parsed and sanitized by Pydantic v2 schemas.
- Invalid enumeration keys, unparsed JSON, or malformed data structures are rejected at the edge with HTTP 422 before touching the repository or database.

### 2.2 SQL Injection Immunity
- The repository layer (`app/repository.py`) exclusively utilizes parameterized SQL statements (`?` placeholders).
- Zero user-supplied parameters are interpolated via Python string formatting (`f"..."`), neutralizing SQL injection vulnerabilities.

### 2.3 Secret Management & Redaction
- The `GEMINI_API_KEY` is ingested via environment variables and is never written to disk, committed to git, or returned through API endpoints.
- Log files and tracebacks redact authentication credentials.

### 2.4 Static File Traversal Defenses
- Static files are served via Starlette's `StaticFiles` handler (`app.mount("/static", ...)`), which enforces strict path resolution and blocks directory traversal attempts (e.g. `../../etc/passwd`).

---

## 3. Security Review & Assessment

For the detailed audit findings, risk classification, and hardening roadmap, see:
- **[Formal Security Review & Audit](security-review.md)**
