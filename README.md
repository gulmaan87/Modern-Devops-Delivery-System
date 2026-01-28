## 🚀 Modern DevOps Delivery System

Simple **FastAPI + React + MongoDB** project to practice modern DevOps workflows.

---

## 🧩 Stack

- **Backend**: FastAPI (Python) with health/status endpoints and MongoDB Atlas
- **Frontend**: React dashboard UI
- **Database**: MongoDB Atlas
- **Infra**: Docker & docker‑compose

---

## ▶️ Run locally

```bash
docker-compose up --build
```

Then open:

- **Frontend**: `http://localhost:3000`
- **Backend**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`

To stop everything:

```bash
docker-compose down
```

---

## 🌐 Live URLs

- **Frontend**: `https://modern-devops-delevery-system-1.onrender.com`

- **Backend API**: `https://modern-devops-delevery-system.onrender.com`
- **Health**: `https://modern-devops-delevery-system.onrender.com/health`
- **Status**: `https://modern-devops-delevery-system.onrender.com/api/status`

---

## 📝 Notes

- Frontend uses `REACT_APP_API_URL` to talk to the backend.
- Backend CORS origins are configured via `CORS_ORIGINS`.

---

## 🔮 Future Improvements

- **Kubernetes deployment** with Helm charts and production-ready manifests
- **Full CI/CD pipeline** (tests, build, deploy) using GitLab CI or GitHub Actions
- **Observability stack** (logging, metrics, tracing) with tools like Prometheus + Grafana
- **Authentication & authorization** for protected API routes
- **More sample features** in the UI (e.g. viewing data from MongoDB)