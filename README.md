# Mentor: The Behavioral Accountability Engine

Mentor is a highly opinionated, strict accountability application designed to enforce daily habits and protocols (like 75 Hard or Monk Mode). It tracks daily execution and actively punishes missed days using a feature called the **Trapdoor**.

## Core Philosophy
- **Stateless & Harsh:** Mentor does not care about feelings. It tracks binary execution (Did you do it or not?).
- **The Trapdoor:** If a user misses a day, the entire application locks down. They cannot access their dashboard, streaks, or commitments until they submit a "Deep Reflection" explaining exactly why they failed.

## Tech Stack
- **Backend:** FastAPI (Python), SQLAlchemy, PostgreSQL
- **Frontend:** Next.js (React), TailwindCSS
- **Authentication:** OAuth2 (Stateless JWT)
- **Deployment Strategy (Upcoming):** Docker, AWS EC2, GitHub Actions CI/CD

## System Architecture

### 1. The Backend (`/Backend`)
The backend is a RESTful API built with FastAPI. 
- **`app/api/`**: Contains all route controllers (endpoints for users, commitments, tracking, daily entries).
- **`app/models/`**: SQLAlchemy ORM models mapping to PostgreSQL tables.
- **`app/schema/`**: Pydantic models for request validation and response serialization.
- **`app/auth/`**: JWT-based stateless authentication logic.

### 2. The Frontend (`/frontend`)
The frontend is a Next.js application built for maximum aesthetic impact (Dark Mode, Deep Reds for penalties).
- **`src/app/page.tsx`**: The main dashboard. It uses a split-screen design. 
  - **Left Panel:** Active Commitments & Tracking Metrics.
  - **Right Panel:** The Execution Log (Historical Timeline).
- **The Trapdoor UI:** An absolute-positioned, un-closable modal (`z-[100]`) that renders if `/missed-days/unresolved` returns any pending missed days.

## Database Schema (PostgreSQL)
*For a visual representation of relationships, we maintain a strict Entity Relationship mapping.*

1. **Users:** The core identity.
2. **Commitments:** A "Protocol" (e.g. "Study for Finals") assigned to a user. Has a `start_date`, `end_date`, and `status`.
3. **TrackingMetrics:** The "Rules" for a commitment (e.g. "Hours >= 8"). Strictly 1-to-Many with Commitments.
4. **DailyEntries:** A user's evening reflection for a specific calendar date (contains mood, sleep, biggest win, biggest failure).
5. **MetricLogs:** The actual execution data. Ties a `TrackingMetric` to a specific `DailyEntry`.
6. **MissedDayReflections:** The penalty log. If a user fails to submit a DailyEntry, they must submit one of these to unlock their account.

## Getting Started (Local Development)

### Backend
```bash
cd Backend
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Current Sprint (Phase 0 / Week 1)
We are currently finalizing the **Analytics Engine** (`Backend/app/api/analytics.py`) to calculate Streaks and Consistency Scores before moving into asynchronous database refactoring and Docker containerization.
