# Mentor: The Behavioral Accountability Engine

[![CI Pipeline](https://github.com/LUFFY-KIngofCoder/Mentor/actions/workflows/ci.yml/badge.svg)](https://github.com/LUFFY-KIngofCoder/Mentor/actions/workflows/ci.yml)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.2+-black.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%26%20RDS-FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)

**Mentor** is a high-conviction, enterprise-grade behavioral accountability platform designed to enforce daily execution protocols (e.g., *75 Hard*, *Monk Mode*). It enforces strict compliance and locks down access upon missed days using an inescapable **Trapdoor Penalty Mechanism**.

---

## 🏛️ System Architecture

Mentor runs on a containerized, decoupled microservice gateway architecture hosted in the cloud:

```
                          Internet (HTTP Port 80)
                                    │
                                    ▼
                         ┌────────────────────┐
                         │   Nginx Gateway    │
                         │ (Reverse Proxy:80) │
                         └─────────┬──────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              │ Path: /                                 │ Path: /api, /docs
              ▼                                         ▼
   ┌──────────────────────┐                  ┌──────────────────────┐
   │  Next.js Frontend    │                  │   FastAPI Backend    │
   │  (React 19 / SSR)    │                  │ (Async Uvicorn ASGI) │
   │  Port 3000 (Internal)│                  │ Port 8000 (Internal) │
   └──────────────────────┘                  └──────────┬───────────┘
                                                        │
                                                        ▼ (SQLAlchemy + Asyncpg)
                                             ┌──────────────────────┐
                                             │  AWS RDS PostgreSQL  │
                                             │ (Managed DB: 5432)   │
                                             └──────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Frontend** | Next.js 16 (App Router), React 19, TypeScript, TailwindCSS, Axios |
| **Backend** | Python 3.10+, FastAPI, Async SQLAlchemy 2.0, Alembic, Pydantic v2 |
| **Database** | Amazon RDS PostgreSQL (`db.t4g.micro`, Free Tier) with `asyncpg` driver |
| **Gateway & Network** | Nginx Reverse Proxy (Alpine), Docker Internal Bridge Network |
| **Containerization** | Docker, Docker Compose (Multi-stage production builds) |
| **CI / CD** | GitHub Actions (`ci.yml`), Pytest unit testing, Docker Hub Registry |
| **Cloud Hosting** | AWS EC2 Linux (`t3.micro`), AWS RDS, AWS IAM Developer Governance |

---

## 🔒 The Core Philosophy: The Trapdoor Engine

1. **Binary Accountability:** Habits are evaluated strictly as Boolean successes or failures at write-time based on target thresholds (`hours >= 8`, `pages >= 10`).
2. **The Trapdoor Lockdown:** If a user fails to submit their evening reflection, the backend flags an unresolved missed day. The frontend mounts an un-closable, full-screen trapdoor modal (`z-[100]`), freezing all dashboards, streaks, and analytics until the user submits a deep psychological reflection explaining their failure.
3. **Write-Time Analytics:** Consistency scores and consecutive streaks are calculated with SQL grouping and backward timestamp analysis.

---

## 📂 Repository Structure

```
Mentor/
├── .github/workflows/          # Automated CI/CD pipelines (Pytest + Docker Hub push)
│   └── ci.yml
├── Backend/                    # FastAPI asynchronous application
│   ├── alembic/                # Database migrations (Dynamic URL override)
│   ├── app/
│   │   ├── api/                # Route controllers (/users, /commitments, /analytics, etc.)
│   │   ├── auth/               # OAuth2 & Stateless JWT token management
│   │   ├── core/               # Security, password hashing, and settings
│   │   ├── db/                 # Async session makers and database engines
│   │   ├── models/             # SQLAlchemy ORM database models
│   │   ├── schema/             # Pydantic validation schemas
│   │   └── utils/              # Timezone utilities and metric calculation logic
│   ├── requirements.txt
│   └── tests/                  # Pytest test suites
├── docker/                     # Production Dockerfiles & Gateway configurations
│   ├── backend/Dockerfile      # Multi-stage Python 3.10 image
│   ├── frontend/Dockerfile     # Next.js AOT production build image
│   └── nginx/nginx.conf        # Gateway routing configuration
├── frontend/                   # Next.js App Router Web Application
│   ├── src/
│   │   ├── app/                # Next.js pages, layouts, and modals
│   │   └── lib/api.ts          # Unified Axios client with JWT auto-injection
│   ├── package.json
│   └── next.config.ts
├── SPRINT_PLAN.md              # 30-Day Enterprise Sprint Execution Plan
└── docker-compose.yml          # Production container orchestration
```

---

## 🚀 Getting Started (Local Development)

### Quickstart with Docker Compose (Recommended)

To run the entire full-stack application (Nginx, FastAPI, Next.js) locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/LUFFY-KIngofCoder/Mentor.git
   cd Mentor
   ```

2. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://<username>:<password>@<rds_or_local_host>:5432/<db_name>
   SECRET_KEY=your_super_secret_jwt_key
   NEXT_PUBLIC_API_URL=/api
   ```

3. **Launch the stack:**
   ```bash
   docker compose up -d --build
   ```

4. **Run database migrations:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Access the application:**
   - **Frontend UI:** `http://localhost/`
   - **Interactive API Docs:** `http://localhost/docs`
   - **API Health Check:** `http://localhost/api/health`

---

## ☁️ Cloud Deployment & Architecture Highlights

- **AOT Production Optimization:** The frontend utilizes `npm run build` with Docker build arguments (`ARG NEXT_PUBLIC_API_URL`) to pre-compile static assets, reducing RAM usage by ~400MB on micro cloud instances.
- **Dedicated Cloud Database (AWS RDS):** Decoupled the database layer from the EC2 compute instance, ensuring data durability, automated AWS snapshots, and multi-AZ failover compatibility.
- **Enterprise IAM Governance:** Configured dedicated developer IAM user roles (`mentor-dev`) with strict permission boundaries to eliminate root account security risks.
- **Unified Gateway Routing:** Standardized all backend services under the `/api` prefix, eliminating CORS preflight overhead and keeping internal service ports isolated from public exposure.

---

## 🧪 Testing & CI/CD

Continuous Integration runs automatically on every push to `main` via GitHub Actions:

```bash
# Run unit tests locally
cd Backend
pytest tests/ -v
```

The pipeline automatically:
1. Provisions an isolated Python environment and installs dependencies.
2. Executes backend unit tests with `pytest`.
3. Compiles multi-stage Docker images for both backend and frontend.
4. Pushes versioned, SHA-tagged images to Docker Hub.

---

## 📄 License
This project is open-source under the MIT License.
