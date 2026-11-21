# Development commands. On Windows run with `mingw32-make <target>`.

ifeq ($(OS),Windows_NT)
	PY := .venv/Scripts/python
	SYS_PY := python
else
	PY := .venv/bin/python
	SYS_PY := python3
endif

.DEFAULT_GOAL := help
.PHONY: help venv install lint format test

help:
	@echo Targets:
	@echo   install  create .venv and install the project with dev and notebook extras
	@echo   lint     run ruff lint and format check
	@echo   format   auto-format and fix lint issues with ruff
	@echo   test     run the test suite

venv:
	$(SYS_PY) -m venv .venv

install: venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e ".[dev,notebook]"
	$(PY) -m pre_commit install

lint:
	$(PY) -m ruff check .
	$(PY) -m ruff format --check .

format:
	$(PY) -m ruff check --fix .
	$(PY) -m ruff format .

test:
	$(PY) -m pytest
