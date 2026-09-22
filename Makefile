PYTHON ?= ../.venv/bin/python
PORT ?= 8000

.PHONY: help run test seed lint clean

help:
	@echo "Personal Command Center (Personal OS)"
	@echo "Usage:"
	@echo "  make run    - Launch the command center on port $(PORT)"
	@echo "  make test   - Run automated test suite via pytest"
	@echo "  make seed   - Populate or reset demonstration data"
	@echo "  make clean  - Remove cache and compiled files"

run:
	$(PYTHON) -m uvicorn app.main:app --host 127.0.0.1 --port $(PORT) --reload

test:
	PYTHONPATH=. $(PYTHON) -m pytest -v tests/

seed:
	PYTHONPATH=. $(PYTHON) -m app.seed_data

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -f *.pyc
