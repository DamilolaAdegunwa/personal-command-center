# Documentation Maintenance Policy & PR Checklists

This document governs documentation lifecycle management for the **Personal Command Center**. It ensures that technical documentation never drifts from source code reality.

---

## 1. Documentation Policy & Guiding Tenets

1. **Documentation is a First-Class Artifact:**  
   No code change modifying an API route, database schema, configuration variable, or business rule will be merged without corresponding documentation updates.
2. **Implementation is Ground Truth:**  
   If documentation and code conflict, the code is treated as evidence of actual behavior. Documentation must be brought into alignment immediately.
3. **No Phantom Features:**  
   Never document functionality that cannot be verified in the repository. Planned features must be explicitly marked as `Roadmap / Planned`.
4. **Mandatory Automated Validation:**  
   All PRs must pass `scripts/validate_docs.py` before merging.

---

## 2. Actionable PR Checklists

### Checklist A: Modifying or Adding an API Endpoint
- [ ] Update route definition and handler in `app/main.py`.
- [ ] If request or response bodies change, update models in `app/models.py`.
- [ ] Update `docs/api/endpoints.md` with the route, method, parameters, and example JSON payloads.
- [ ] If new schemas were introduced, document them in `docs/api/schemas.md`.
- [ ] Add integration test coverage in `tests/test_api.py`.
- [ ] Run `python3 scripts/validate_docs.py` to verify endpoint parity.
- [ ] Append entry in `docs/CHANGELOG.md`.

### Checklist B: Modifying Database Schema or Indexes
- [ ] Update table DDL or index statements in `app/database.py` (`init_db`).
- [ ] Update corresponding Pydantic models in `app/models.py`.
- [ ] Update SQL queries in `app/repository.py`.
- [ ] Update the ER diagram and table specification in `docs/database/schema.md`.
- [ ] If query performance characteristics change, update `docs/database/queries-and-performance.md`.
- [ ] If seed records are affected, update `app/seed_data.py`.
- [ ] Update `docs/documentation-traceability.md`.

### Checklist C: Introducing Configuration Variables
- [ ] Add variable extraction logic in relevant Python module or shell script.
- [ ] Document the variable in `docs/configuration/index.md` (Name, Purpose, Type, Default, Sensitivity).
- [ ] If secret, verify it is excluded from git and omitted from log statements.
- [ ] Update example environment declarations in `docs/development/local-setup.md`.

### Checklist D: Modifying System Architecture or Runtime Flow
- [ ] Update architecture diagrams in `docs/architecture/system-architecture.md` or `component-architecture.md`.
- [ ] Update sequence diagrams in `docs/architecture/runtime-flows.md`.
- [ ] Update the repository structure guide in `docs/codebase-map.md`.

---

## 3. Automated Pre-Commit Verification

Before submitting changes, run the validation tool:

```bash
# Validate internal links and endpoint parity
python3 scripts/validate_docs.py

# Run test suite including documentation validation
PYTHONPATH=. pytest -v tests/
```
