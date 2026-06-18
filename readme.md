# Inventory & Order Management API (FastAPI Backend)

A production-ready Python backend implementing clean architecture, custom API response exceptions, a global error handling layout, pagination middleware, and containerized deployment.

---

## 1. Quick Start with Docker Compose

The database and backend services are fully containerized and configured via `docker-compose.yml` in the project root. All database configuration values are dynamic and can be injected at startup.

### Run with Default Environment Values
To build and start all services using default PostgreSQL credentials (`postgres`/`postgres`):
```bash
# Execute from the project root directory containing docker-compose.yml
docker compose up --build -d
```
*On start, the backend container will automatically run the database CLI tool to initialize the database tables from [baseline_schema.sql](app/migrations/baseline_schema.sql) if they do not exist.*

### Run by Injecting Custom Environment Variables
You can override credentials at run-time by passing host environment variables directly to the Docker Compose command:
```bash
# Run with custom PostgreSQL password and port
DB_PASSWORD=my_secure_password DB_PORT=5433 DB_NAME=inventory_db docker compose up --build -d
```

### Run using a Root-level `.env` File
Alternatively, create a `.env` file in the project root directory next to `docker-compose.yml`:
```env
DB_USER=admin
DB_PASSWORD=secretpassword
DB_NAME=custom_inventory
DB_PORT=5432
```
Docker Compose will automatically pick up this file and interpolate the variables into the containers when you run:
```bash
docker compose up --build -d
```

To stop all running containerized services and preserve persistent data:
```bash
docker compose down
```

---

## 2. Local Manual Setup

To run the backend directly on your local host (outside Docker):

### Setup Virtual Environment
```bash
cd inventory-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database Schema Initialization (CLI)
You can initialize the database schema manually by executing the database script helper with the `--init-db` flag:
```bash
python -m app.database.database --init-db
```

### Running the API Server
Start the development server with live reload:
```bash
uvicorn app.main:app --reload
```
Access the interactive API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 3. Core Features & Architecture

### Custom Exception Handler
The API uses custom domain exceptions inheriting from `AppException` (under `app/utils/exceptions`). This translates service-level exceptions directly to clean JSON responses:
```json
{
  "detail": "Customer not found.",
  "error_code": "CUSTOMER_NOT_FOUND"
}
```

### Cursor-Based Pagination
Supports cursor-based query pagination:
* **Database level**: Via the query helper function `paginate_query`.
* **In-memory level**: Via a zero-config FastAPI middleware (`PaginationMiddleware`) that automatically paginates and wraps list responses in standard envelopes when calling any `GET` endpoint with the parameter `?paginate=true` (e.g. `/customers?paginate=true&limit=5&sort_by=id&order=desc`).

### Generic API Responses
Exposes the generic `APIResponse[T]` utility model (under `app/utils/response`) to package success operations inside a unified JSON layout:
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": { ... }
}
```
