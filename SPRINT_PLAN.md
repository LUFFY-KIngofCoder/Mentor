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

## Phase 1: Async PostgreSQL (COMPLETED ✅)

### Goal
Replace synchronous SQLAlchemy engine with `asyncpg` to allow FastAPI to handle thousands of concurrent requests without blocking.

### What Was Built
- Replaced `psycopg2` with `asyncpg` across backend
- Converted database session maker to `create_async_engine` + `AsyncSession`
- Updated all API routes to `async def` with `await db.execute(select(...))`
- Solved N+1 query problem using `selectinload(Commitment.metrics)`

---

## Phase 2: Docker Containerization (COMPLETED ✅)

### Goal
Package the application into reproducible Docker containers.

### What Was Built
- Multi-stage `Dockerfile` for FastAPI backend and optimized production Next.js frontend
- `docker-compose.yml` orchestrating services, networks, and environments
- Implemented build arguments (`ARG NEXT_PUBLIC_API_URL`) for Ahead-Of-Time frontend bundle optimization

---

## Phase 3: CI/CD Pipeline (COMPLETED ✅)

### Goal
Automate testing and container image publishing on GitHub Actions.

### What Was Built
- `.github/workflows/ci.yml` pipeline triggering on push to `main`
- Automated test runs with `pytest`
- Automated multi-platform Docker image build and push to Docker Hub with commit SHA tagging

---

## Phase 4: AWS Cloud Deployment & RDS Gateway Architecture (COMPLETED ✅)

### Goal
Deploy the application live to AWS with dedicated database persistence and gateway routing.

### What Was Built & Exceeded
- **Compute:** EC2 instance running containerized microservices
- **Managed Database:** Migrated from local container to dedicated **AWS RDS PostgreSQL** (`db.t4g.micro` in `ap-south-1`)
- **Gateway Reverse Proxy:** Configured **Nginx** reverse proxy on port 80 routing `/` to Next.js and `/api`, `/docs` to FastAPI
- **Security & Governance:** IAM Developer account configuration (`mentor-dev`), VPC Security Groups, and dynamic Alembic URL injection

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
