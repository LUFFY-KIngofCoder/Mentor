# Mentor: 30-Day Enterprise Sprint Plan

Transform Mentor from a local dev project into a production-grade, containerized AI SaaS.

---

## Phase 0: Analytics Baseline (COMPLETED ✅)

### Goal
Build the analytics engine before touching infrastructure, so we have a working feature to deploy.

### What Was Built
- **`is_successful` column** added to `MetricLog` via Alembic migration (with `server_default` fix)
- **Write-Time Calculation**: `daily_entry.py` now evaluates and persists `is_successful` at the point of entry
- **Helper Utility**: `app/utils/metric.py` → `evaluate_metric_success()` for reusable, testable logic
- **Analytics Query**: `app/api/analytics.py` uses `GROUP BY` + `HAVING func.count() == required_metric_count` to correctly identify days where **all** required metrics were completed
- **Streak Logic**: Walk backward from today (or yesterday) through the sorted `successful_dates` list
- **Schema**: `app/schema/analytics.py` → `AnalyticMetrics` and `CommitmentAnalyticsResponse` Pydantic models
- **Frontend**: Dynamic multi-metric creation in the New Commitment Modal (`page.tsx`)

### Metrics Computed
| Metric | Logic |
|---|---|
| `total_active_days` | `min((today - start_date).days + 1, duration_days)` |
| `successful_days` | Days where ALL metrics were `is_successful == True` |
| `consistency_score` | `(successful_days / total_active_days) * 100` |
| `streak` | Consecutive successful days ending today or yesterday |

---

## Phase 1: Async PostgreSQL (Week 1)

### Goal
Replace synchronous SQLAlchemy engine with `asyncpg` to allow FastAPI to handle thousands of concurrent requests without blocking.

### Changes Required
- Replace `psycopg2` with `asyncpg` in `requirements.txt`
- Update `DATABASE_URL` in `.env` from `postgresql://` → `postgresql+asyncpg://`
- Replace `create_engine` + `SessionLocal` in `app/db/session.py` with `create_async_engine` + `AsyncSession`
- Update all API route functions from `def` → `async def`
- Replace all `db.query(...)` calls with `await db.execute(select(...))`
- Fix N+1 Problem on `com.metrics` → Use `selectinload(Commitment.metrics)` via `options()`

### Key Imports
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from sqlalchemy.orm import selectinload
```

---

## Phase 2: Docker Containerization (Week 2)

### Goal
Package the entire application (FastAPI backend + Next.js frontend + PostgreSQL) into a reproducible, portable Docker environment so it runs identically on any machine or server.

### Files to Create
- **`Backend/Dockerfile`** — Multi-stage build for the FastAPI app
- **`frontend/Dockerfile`** — Multi-stage build for the Next.js app
- **`docker-compose.yml`** (project root) — Orchestrates all 3 services: `db`, `backend`, `frontend`
- **`.dockerignore`** files — Exclude `venv`, `node_modules`, `__pycache__` from builds

### `docker-compose.yml` Service Architecture
```
db (postgres:16-alpine)
  └── Persistent Volume: postgres_data
backend (FastAPI / Uvicorn)
  └── Depends on: db
  └── Env: DATABASE_URL, SECRET_KEY
frontend (Next.js)
  └── Depends on: backend
  └── Env: NEXT_PUBLIC_API_URL
```

---

## Phase 3: CI/CD Pipeline (Week 3)

### Goal
Automate testing and deployment using GitHub Actions. Every push to `main` automatically tests, builds Docker images, and pushes them to Docker Hub (registry).

### Files to Create
- **`.github/workflows/ci.yml`** — GitHub Actions pipeline

### Pipeline Steps
1. **Trigger**: On every `git push` to `main`
2. **Test**: Run `pytest` against backend
3. **Build**: `docker build` for both backend and frontend images
4. **Push**: Push images to Docker Hub with the commit SHA as the tag

---

## Phase 4: AWS Cloud Deployment (Week 4)

### Goal
Deploy the Dockerized application to a live, publicly accessible AWS server — entirely on the **AWS Free Tier** at zero cost.

### AWS Services Used (All Free Tier)
| Service | Usage | Free Tier Limit |
|---|---|---|
| **EC2** | 1x `t2.micro` Linux server to run Docker | 750 hrs/month |
| **S3** | Object storage (for future file uploads) | 5 GB |
| **Security Groups** | Firewall rules (allow ports 80, 443, 22) | Free |

### Deployment Architecture
```
Internet → AWS Security Group (Firewall)
         → EC2 t2.micro (Ubuntu 24.04)
           └── Docker Compose
               ├── Nginx (Reverse Proxy) → Port 80/443
               ├── FastAPI Backend       → Internal Port 8000
               ├── Next.js Frontend      → Internal Port 3000
               └── PostgreSQL DB         → Internal Port 5432
                   └── EBS Volume (Persistent Storage)
```

### Deployment Steps
1. Create AWS account + IAM user with EC2 permissions
2. Launch `t2.micro` EC2 instance with Ubuntu 24.04
3. Configure Security Groups to allow HTTP (80), HTTPS (443), SSH (22)
4. SSH into the instance and install Docker + Docker Compose
5. Clone the GitHub repo onto the server
6. Create production `.env` file on the server
7. Run `docker compose up -d --build` to launch all services
8. Configure a domain name (optional) and SSL via Let's Encrypt / Certbot

> AWS Free Tier is available for 12 months for all new AWS accounts. The `t2.micro` instance is more than sufficient to run the entire Mentor stack.

---

## Architecture Overview

```
Commitment
  └── 1:M TrackingMetric
         └── 1:M MetricLog
                └── is_successful: bool (Write-Time, computed in daily_entry.py)

Analytics Query Flow:
  MetricLog (is_successful=True) → GROUP BY date → HAVING count == required_metrics
  → successful_dates[] → streak loop (walk backward from today)
```
