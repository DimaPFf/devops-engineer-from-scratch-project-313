install:
	uv sync
start:
	FLASK_APP=src.main uv run flask run --port 8080 --debug

start-prod:
	FLASK_APP=src.main sh -c 'uv run flask run --host=0.0.0.0 --port=$$PORT'

lint:
	uv run ruff check src

lint-fix:
	uv run ruff check --fix src

test:
	uv run pytest -v

install-front:
	npm install @hexlet/project-devops-deploy-crud-frontend

start-front:
	npx start-hexlet-devops-deploy-crud-frontend

start-project:
	npx concurrently -k -n "FRONT,BACK" -c "blue,green"\
			"make start-front" \
			"make start"
