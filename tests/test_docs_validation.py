import subprocess
import sys
from pathlib import Path

def test_documentation_system_integrity():
    """Verify that all documentation files exist, links resolve, and routes match."""
    repo_root = Path(__file__).parent.parent.resolve()
    validator_script = repo_root / "scripts" / "validate_docs.py"
    
    assert validator_script.exists(), "scripts/validate_docs.py must exist"

    result = subprocess.run(
        [sys.executable, str(validator_script)],
        cwd=str(repo_root),
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
        
    assert result.returncode == 0, f"Documentation validation failed:\n{result.stdout}\n{result.stderr}"
