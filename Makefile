.PHONY: run init-db seed seed-force install docker-up docker-down docker-setup

# Configuration variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
UVICORN = $(VENV_DIR)/bin/uvicorn
PIP = $(VENV_DIR)/bin/pip

# 1. Start the FastAPI development server with hot-reload
run:
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Initialize database schema (executes baseline_schema.sql)
init-db:
	$(PYTHON) -m app.database.database --init-db

# 3. Seed database tables (50 products, 5 customers, 5 orders)
seed:
	$(PYTHON) -m app.database.seeds.seed

# 4. Force-reset and seed database tables
seed-force:
	$(PYTHON) -m app.database.seeds.seed --force

# 5. Install virtualenv requirements
install:
	$(PIP) install -r requirements.txt

# 6. Build and start services using Docker Compose
docker-up:
	docker compose up --build -d

# 7. Stop Docker Compose services
docker-down:
	docker compose down

# 8. Start backend/db, initialize schema, and seed mock data
docker-setup:
	docker compose up --build -d
	docker compose run --rm backend python -m app.database.database --init-db
	docker compose run --rm backend python -m app.database.seeds.seed
