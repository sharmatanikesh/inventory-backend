# Inventory Management System (React Frontend)

This is the React frontend for the Inventory & Order Management System. It is built using Vite, Tailwind CSS, and standard components.

---

## 1. Environment & API Architecture

The frontend is configured with a reverse proxy using Vite. Any request made to `/api/*` is proxied to the backend API.

* **Local Frontend Server**: `http://localhost:5173`
* **Local Backend API (Target)**: `http://localhost:8000`
* **Live Production Frontend (Vercel)**: [https://inventory-frontend-olive.vercel.app](https://inventory-frontend-olive.vercel.app)
* **Live Production Backend API (Railway)**: `https://inventory-backend-production-03bc.up.railway.app`

---

## 2. Running Standalone via Docker

To build and run the frontend inside a Docker container, follow these steps:

### Build the Image
From the `inventory-frontend` directory, build the Docker container image:
```bash
docker build -t inventory-frontend .
```

### Run the Container
Because the backend runs on the host (port `8000`), the frontend container needs to route proxy requests to the host's localhost.

* **For macOS & Windows**:
  Run the container and pass `BACKEND_API_URL` pointing to the host's network gateway:
  ```bash
  docker run -d \
    -p 5173:5173 \
    -e BACKEND_API_URL=http://host.docker.internal:8000 \
    --name inventory_frontend \
    inventory-frontend
  ```

* **For Linux**:
  Add the `--add-host` flag to resolve the host's loopback interface:
  ```bash
  docker run -d \
    -p 5173:5173 \
    --add-host=host.docker.internal:host-gateway \
    -e BACKEND_API_URL=http://host.docker.internal:8000 \
    --name inventory_frontend \
    inventory-frontend
  ```

### Verify Deployment
* Open **[http://localhost:5173](http://localhost:5173)** in your browser to view the application.
* The frontend will make calls to `/api/...` which will be forwarded to the backend running at `http://localhost:8000`.

---

## 3. Stopping the Container

To stop and remove the running frontend container, execute:
```bash
docker stop inventory_frontend && docker rm inventory_frontend
```

---

## 4. Local Manual Setup (Without Docker)

If you want to run the Vite dev server directly on your host machine:

### Install Dependencies
```bash
npm install
```

### Configure environment
Create a `.env` file in the root of the `inventory-frontend` folder:
```env
PORT=5173
BACKEND_API_URL=http://localhost:8000
```

### Start Development Server
```bash
npm run dev
```
The application will be live at `http://localhost:5173`.
