# Inventory & Order Management System

A full-stack Inventory & Order Management System featuring a containerized FastAPI backend and a React frontend.

---

## 🌐 Live Deployments

* **Frontend Web App**: [https://inventory-bay-two.vercel.app/](https://inventory-bay-two.vercel.app/)
* **Backend API Gateway**: [https://inventory-production-f58d.up.railway.app](https://inventory-production-f58d.up.railway.app)
* **Backend Swagger API Docs**: [https://inventory-production-f58d.up.railway.app/docs](https://inventory-production-f58d.up.railway.app/docs)

---

## 🔑 Authentication / Accessing the Application

When accessing the frontend application (either local or production), a **quick-fill button** is provided on the Login Page for testing and evaluation.

> [!IMPORTANT]
> Please use the **Admin Staff Demo Account** auto-fill button on the login screen.
> 
> If you wish to enter credentials manually, use the following:
> * **Email**: `admin@example.com`
> * **Password**: `admin1234`

---

## 💻 Local Development Setup

To run and modify the backend or frontend services individually on your host machine, checkout their respective setup guides:

1. **Backend Service**: See [backend/readme.md](file:///Users/tanikesh/Documents/ethara/inventory/backend/readme.md) for details on setting up the python virtual environment, installing dependencies, configuring PostgreSQL, and launching the FastAPI development server.
2. **Frontend Service**: See [frontend/README.md](file:///Users/tanikesh/Documents/ethara/inventory/frontend/README.md) for instructions on installing NPM packages and starting the Vite development server.

---

## 🐳 Quick Start with Docker Compose

You can boot up the entire stack—PostgreSQL database, FastAPI backend, and React frontend—with a single Docker Compose execution.

The root configuration file [docker-compose.yml](file:///Users/tanikesh/Documents/ethara/inventory/docker-compose.yml) is configured to manage the network routing, ports, and lifecycle of all services.

### Step 1: Start the Containers
Run the following command in the root folder (where `docker-compose.yml` is located):
```bash
docker compose up --build -d
```
*Note: Upon startup, the backend container automatically initializes the baseline database schema.*

### Step 2: Seed the Database
To populate the Postgres database with mock data (including products, customers, orders, and the default administrator login), execute the database seeding script directly inside the running backend container:
```bash
docker compose exec backend python -m app.database.seeds.seed
```

Alternatively, if you want to reset the database and seed fresh data, you can pass the `--force` flag:
```bash
docker compose exec backend python -m app.database.seeds.seed --force
```

### Step 3: Accessing the Local Services
* **Frontend Application**: [http://localhost:5173](http://localhost:5173)
* **Backend API Gateway**: [http://localhost:8000](http://localhost:8000)
* **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 4: Tear Down
To stop the services and remove containers:
```bash
docker compose down -v
```
