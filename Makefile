# Development commands. On Windows run with `mingw32-make <target>`.

ifeq ($(OS),Windows_NT)
	PY := .venv/Scripts/python
	SYS_PY := python
else
	PY := .venv/bin/python
	SYS_PY := python3
endif

.DEFAULT_GOAL := help
.PHONY: help venv install lint format test data interim

help:
	@echo Targets:
	@echo   install  create .venv and install the project with dev and notebook extras
	@echo   lint     run ruff lint and format check
	@echo   format   auto-format and fix lint issues with ruff
	@echo   test     run the test suite
	@echo   data     download the raw Kaggle dataset into data/raw
	@echo   interim  merge raw files into data/interim/train_merged.parquet

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

data:
	$(PY) -m wastewise.data.download

interim: data
	$(PY) -m wastewise.data.load
