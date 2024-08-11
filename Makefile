TEST_DIR = tests
PRJ = yhttp.ext.dbmanager
PYTEST_FLAGS = -v
HERE = $(shell readlink -f `dirname .`)
VENVNAME = $(shell basename $(HERE) | cut -d'-' -f1)
VENV = $(HOME)/.virtualenvs/$(VENVNAME)
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
PYTEST = $(VENV)/bin/pytest
COVERAGE = $(VENV)/bin/coverage
FLAKE8 = $(VENV)/bin/flake8
TWINE = $(VENV)/bin/twine


.PHONY: test
test:
	$(PYTEST) $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	$(PYTEST) $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


.PHONY: cover-html
cover-html: cover
	$(COVERAGE) html
	@echo "Browse htmlcov/index.html for the covearge report"


.PHONY: lint
lint:
	$(FLAKE8)


.PHONY: venv
venv:
	$(PY) -m venv $(VENV)


.PHONY: env
env:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .


.PHONY: sdist
sdist:
	$(PY) -m build --sdist


.PHONY: bdist
wheel:
	$(PY) -m build --wheel


.PHONY: dist
dist: sdist wheel


.PHONY: pypi
pypi: dist
	$(TWINE) upload dist/*.gz dist/*.whl


.PHONY: clean
clean:
	rm -rf build/*
