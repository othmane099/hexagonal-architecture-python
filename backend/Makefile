PYTHON=./.venv/bin/python

PHONY = help install format test migrations migrate run

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To format code type -> make format"
	@echo "To test the project type -> make test"
	@echo "To create database migrations type -> make migrations"
	@echo "To run database migrations type -> make migrate"
	@echo "To run the project type -> make run"
	@echo "------------------------------------"


install:
	${PYTHON} -m pip install -r requirements.txt

format:
	${PYTHON} -m isort src tests --force-single-line-imports
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config pyproject.toml
	${PYTHON} -m isort src tests
test:
	TEST_RUN="TRUE" ${PYTHON} -m pytest tests

migrations:
	alembic -c alembic.ini revision --autogenerate

migrate:
	alembic -c alembic.ini upgrade head

run:
	${PYTHON} -m uvicorn src.sms.adapters.entry_points.api.app:app --host 0.0.0.0 --port 8000 --reload