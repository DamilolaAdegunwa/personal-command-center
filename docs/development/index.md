# Developer Experience (DX) Overview

This directory provides comprehensive documentation for engineering and contributing to the **Personal Command Center**.

---

## 1. Engineering Philosophy

The Personal Command Center is engineered with a **zero-drag, instant-feedback** developer experience:

- **Zero Build Step:** The frontend uses native modern browser capabilities (ES Modules, CSS Variables, SVG). You edit JavaScript or CSS in `static/` and simply refresh your browser.
- **Fast Startup:** The Uvicorn ASGI server boots in less than 400 milliseconds.
- **Single Dependency File:** Python dependencies are minimal, modern, and pinned in `requirements.txt`.
- **Self-Seeding Runtime:** Running `app.main` automatically creates the SQLite database and populates high-fidelity demonstration records if the database is uninitialized.
- **Integrated Interactive Documentation:** FastAPI automatically renders live Swagger UI documentation at `http://127.0.0.1:8000/docs` and ReDoc at `http://127.0.0.1:8000/redoc`.

---

## 2. Toolchain Reference

| Tool | Version | Purpose in Project |
|---|---|---|
| **Python** | 3.14+ | Core runtime language |
| **FastAPI** | >= 0.115.0 | High-performance asynchronous web framework |
| **Uvicorn** | >= 0.30.0 | Lightweight ASGI production web server |
| **Pydantic** | >= 2.8.0 | Strict runtime schema parsing and validation |
| **aiosqlite** | >= 0.20.0 | Asynchronous SQLite interface |
| **pytest** | >= 8.0.0 | Unit and integration testing framework |
| **httpx** | >= 0.27.0 | Test client transport for FastAPI |
| **google-genai** | >= 2.0.0 | Official Google GenAI SDK for Gemini 2.5 Flash |

---

## 3. Developer Documentation Guides

- **[Local Setup & Bootstrapping](local-setup.md):** Prerequisites, virtual environment creation, dependency installation, and verification.
- **[Development Workflows](workflows.md):** Common tasks, running tests, database seeding, and interactive debugging.
- **[Engineering Conventions](conventions.md):** Code style, typing rules, SQL query standards, and testing patterns.
