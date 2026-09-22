#!/usr/bin/env python3
"""
Automated Documentation Validation Tool for Personal Command Center.
Validates:
1. Presence of all mandatory documentation files.
2. Internal Markdown link integrity (zero dead local links).
3. Parity between FastAPI routes in app/main.py and docs/api/endpoints.md.
"""
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = REPO_ROOT / "docs"

MANDATORY_DOC_FILES = [
    "README.md",
    "docs/README.md",
    "docs/index.md",
    "docs/DOCUMENTATION-AUDIT.md",
    "docs/business-rules.md",
    "docs/codebase-map.md",
    "docs/glossary.md",
    "docs/faq.md",
    "docs/documentation-traceability.md",
    "docs/documentation-maintenance.md",
    "docs/CHANGELOG.md",
    "docs/architecture/index.md",
    "docs/architecture/system-architecture.md",
    "docs/architecture/component-architecture.md",
    "docs/architecture/data-flow.md",
    "docs/architecture/runtime-flows.md",
    "docs/api/index.md",
    "docs/api/endpoints.md",
    "docs/api/schemas.md",
    "docs/development/index.md",
    "docs/development/local-setup.md",
    "docs/development/workflows.md",
    "docs/development/conventions.md",
    "docs/configuration/index.md",
    "docs/database/index.md",
    "docs/database/schema.md",
    "docs/database/queries-and-performance.md",
    "docs/integrations/index.md",
    "docs/messaging/index.md",
    "docs/testing/index.md",
    "docs/deployment/index.md",
    "docs/operations/runbook.md",
    "docs/operations/troubleshooting.md",
    "docs/security/index.md",
    "docs/security/security-review.md",
]

def check_mandatory_files():
    print("[1/3] Checking presence and non-emptiness of mandatory documentation files...")
    missing = []
    empty = []
    for rel_path in MANDATORY_DOC_FILES:
        p = REPO_ROOT / rel_path
        if not p.exists():
            missing.append(rel_path)
        elif p.stat().st_size == 0:
            empty.append(rel_path)

    if missing:
        print(f"  ❌ ERROR: Missing {len(missing)} documentation files:")
        for m in missing:
            print(f"     - {m}")
        return False
    if empty:
        print(f"  ❌ ERROR: Found {len(empty)} empty documentation files:")
        for e in empty:
            print(f"     - {e}")
        return False

    print(f"  ✅ All {len(MANDATORY_DOC_FILES)} mandatory documentation files present and populated.")
    return True

def check_markdown_links():
    print("[2/3] Validating internal Markdown link integrity...")
    all_md_files = list(DOCS_DIR.rglob("*.md")) + [REPO_ROOT / "README.md"]
    broken_links = []

    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    for md_file in all_md_files:
        content = md_file.read_text(encoding="utf-8")
        # Strip code blocks to avoid false positives in code snippets
        content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content_no_code = re.sub(r'`[^`]+`', '', content_no_code)

        for match in link_pattern.finditer(content_no_code):
            text, target = match.groups()
            target = target.strip()

            # Skip external web links, mailto, anchor-only links
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            # Strip target anchors if present (e.g. file.md#section)
            target_clean = target.split("#")[0]
            if not target_clean:
                continue

            resolved_path = (md_file.parent / target_clean).resolve()
            if not resolved_path.exists():
                broken_links.append((md_file.relative_to(REPO_ROOT), target, text))

    if broken_links:
        print(f"  ❌ ERROR: Found {len(broken_links)} broken internal Markdown links:")
        for source_file, target, text in broken_links:
            print(f"     - in '{source_file}': [{text}]({target}) does not resolve to an existing file")
        return False

    print("  ✅ All internal Markdown links resolve to existing files.")
    return True

def check_api_route_parity():
    print("[3/3] Validating FastAPI route parity against docs/api/endpoints.md...")
    main_py = REPO_ROOT / "app" / "main.py"
    endpoints_md = REPO_ROOT / "docs" / "api" / "endpoints.md"

    if not main_py.exists() or not endpoints_md.exists():
        print("  ❌ ERROR: app/main.py or docs/api/endpoints.md missing.")
        return False

    main_content = main_py.read_text(encoding="utf-8")
    doc_content = endpoints_md.read_text(encoding="utf-8")

    # Extract all routes defined via @app.(get|post|put|delete)("...")
    route_pattern = re.compile(r'@app\.(get|post|put|delete)\("([^"]+)"')
    routes = route_pattern.findall(main_content)

    undocumented = []
    for method, path in routes:
        # Check if route pattern appears in documentation
        # e.g., "GET /api/today" or "/api/projects/{project_id}"
        pattern_check = path
        # Also normalize path variables like {project_id}
        if pattern_check not in doc_content and path not in doc_content:
            undocumented.append((method.upper(), path))

    if undocumented:
        print(f"  ❌ ERROR: Found {len(undocumented)} undocumented routes in docs/api/endpoints.md:")
        for method, path in undocumented:
            print(f"     - {method} {path}")
        return False

    print(f"  ✅ All {len(routes)} FastAPI routes are accounted for in docs/api/endpoints.md.")
    return True

def main():
    print("==================================================")
    print(" 🛰️  PERSONAL COMMAND CENTER DOCUMENTATION VALIDATOR")
    print("==================================================")

    res1 = check_mandatory_files()
    res2 = check_markdown_links()
    res3 = check_api_route_parity()

    print("==================================================")
    if res1 and res2 and res3:
        print("🎉 SUCCESS: All documentation validation checks PASSED.")
        print("==================================================")
        return 0
    else:
        print("❌ FAILURE: Documentation validation checks failed.")
        print("==================================================")
        return 1

if __name__ == "__main__":
    sys.exit(main())
