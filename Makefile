TEST_DIR = tests
PRJ = yhttp.ext.dbmanager
PYTEST_FLAGS = -v
HERE = $(shell readlink -f `dirname .`)
VENVNAME = $(shell basename $(HERE) | cut -d'-' -f1)
VENV = $(HOME)/.virtualenvs/$(VENVNAME)
PY = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3
PYTEST = $(VENV)/bin/pytest
FLAKE8 = $(VENV)/bin/flake8
TWINE = $(VENV)/bin/twine


.PHONY: test
test:
	$(PYTEST) $(PYTEST_FLAGS) $(TEST_DIR)


.PHONY: cover
cover:
	$(PYTEST) $(PYTEST_FLAGS) --cov=$(PRJ) $(TEST_DIR)


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
	$(PY) setup.py sdist


.PHONY: bdist
bdist:
	$(PY) setup.py bdist_egg


.PHONY: dist
dist: sdist bdist


.PHONY: pypi
pypi: dist
	$(TWINE) upload dist/*.gz dist/*.egg


.PHONY: clean
clean:
	rm -rf build/*
