install:
	uv sync
start:
	FLASK_APP=src.main uv run flask run --port 8080 --debug

lint:
	uv run ruff check src

lint-fix:
	uv run ruff check --fix src

test:
	uv run pytest