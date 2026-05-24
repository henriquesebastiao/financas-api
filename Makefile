help: # Show targets
	@awk 'BEGIN {FS = ":.*#"} /^[a-zA-Z_-]+:.*#/ {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint: # Run linters
	uv run ruff check .; uv run ruff check . --diff; uv run ruff format --check .

format: # Format code
	uv run ruff format .; uv run ruff check . --fix

test: # Run tests with coverage
	uv run pytest -s -x --cov=app -v; uv run coverage html

sync: # Sync dependencies
	uv sync --all-groups
	uv export --no-hashes --no-dev -o requirements.txt

export: # Export app dependencies to requirements.txt
	uv export --no-hashes --no-dev -o requirements.txt

up: # Start local Postgres via docker compose
	docker compose up -d

up-db: # Start local Postgres and initialize database
	docker compose up database -d

down: # Stop local Postgres
	docker compose down

migrate: # Apply pending migrations
	uv run alembic upgrade head

migrate-new: # Generate new migration (use msg="...")
	uv run alembic revision --autogenerate -m "$(msg)"

dev: # Run FastAPI development server with auto-reload
	uv run fastapi dev app/main.py --reload

deps: # Show direct dependencies
	uv tree --no-dev -d 1

deps-dev: # Show development dependencies
	uv tree --only-dev -d 1

.PHONY: \
	lint \
	format \
	test \
	sync \
	export \
	up \
	up-db \
	down \
	migrate \
	migrate-new \
	dev \
	deps \
	deps-dev \
	help