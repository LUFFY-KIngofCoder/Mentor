# Phase 1: Advanced Backend Engineering - Implementation Plan

This plan breaks down the comprehensive "Advanced Backend Engineering" requirements into a structured, sequential roadmap tailored specifically for the **Mentor** application. Our goal is to transform the Mentor backend from a "working" state into a deeply engineered, production-ready system. 

> [!IMPORTANT]
> **Core Philosophy**: 
> 1. We prioritize **depth over speed**. We must be able to explain, test, break, and defend every design decision we make.
> 2. **Testing is Continuous**: No feature in any epic is considered complete until its relevant tests exist.

---

## Detailed Epics Roadmap (Mentor Specific)

We will implement this directly into the `Mentor` codebase, step by step.

### Epic 1: Architectural Foundation (Service & Repositories) ✅
**Goal:** Stop writing SQL and business logic directly inside our FastAPI routers (`app/api/*.py`).
*   **Action 1 (Exceptions):** Create `app/core/exceptions.py`. Define standard errors like `CommitmentNotFound`, `UnauthorizedAccess`, and a global FastAPI handler to return them as `{ "error": "CODE", "message": "..." }`.
*   **Action 2 (Users & Auth):** Build `UserRepository` (handles SQLAlchemy) and `UserService` (handles password hashing). Refactor the `/api/users` and `/api/auth` routers.
*   **Action 3 (Commitments & Analytics):** Build `CommitmentRepository` and `AnalyticsService`. Move the complex streak calculation logic out of the router and into the Service layer. Define strict transaction boundaries (when we `commit()`).
*   **Action 4 (Tests):** Write unit tests for `AnalyticsService` and integration tests for `CommitmentRepository`.

### Epic 2: Observability, APM & Lifecycle ✅
**Goal:** Know exactly what happens to a request from the moment it hits the server to the moment it leaves, and catch unhandled crashes automatically.
*   **Action 1 (Sentry Integration):** Install and configure the Sentry SDK to automatically capture exceptions and performance traces (APM) in production.
*   **Action 2 (Request IDs):** Create a middleware that generates a unique `request_id` (UUID) for every incoming request.
*   **Action 3 (Structured Logging):** Replace `print()` with Python's `logging` configured to output JSON (for CloudWatch ingestion). Every log must include the `request_id`, HTTP method, endpoint, and execution time.
*   **Action 4 (Lifecycle):** Configure FastAPI startup and shutdown events to cleanly open and close the PostgreSQL connection pools.

### Epic 3: Authorization & API Engineering ✅
**Goal:** Ensure a user can never touch another user's data, and build standard REST patterns.
*   **Action 1 (Resource Ownership):** Enforce tenant isolation. A user fetching `GET /api/commitments/{id}` must prove they own that specific commitment, not just that they are logged in.
*   **Action 2 (Pagination & Filtering):** Update `GET /api/commitments` to implement **Cursor Pagination** (`cursor` and `size`) for infinite scrolling, bypassing the slow `OFFSET` method.
*   **Action 3 (Response Schemas):** Strictly type all outputs using Pydantic so we never accidentally leak password hashes or internal DB IDs.

### Epic 4: Database Performance & Async Mastery
**Goal:** Prove our async database is actually fast by analyzing its execution.
*   **Action 1 (Query Plans):** Use PostgreSQL `EXPLAIN ANALYZE` on our heaviest query (the Analytics streak calculation). 
*   **Action 2 (Indexes):** Add composite indexes to `MetricLog.date` and `MetricLog.is_successful` via Alembic to speed up the streak query.
*   **Action 3 (Async Concurrency):** Build a dashboard endpoint that fetches User Profile, Active Commitments, and Streak Analytics *concurrently* using `asyncio.gather()` rather than sequentially. Measure the speed difference.

### Epic 5: Redis Integration
**Goal:** Introduce in-memory caching and abuse prevention.
*   **Action 1 (Caching):** The Analytics streak calculation is heavy. When a user requests it, cache the result in Redis with a 1-hour TTL. Invalidate this cache immediately if the user logs a new `daily_entry`.
*   **Action 2 (Rate Limiting):** Implement a Redis-backed token bucket rate limiter to restrict `/api/auth/login` to 5 requests per minute per IP to prevent brute-force attacks.

### Epic 6: Background Jobs & Reliability
**Goal:** Offload slow tasks from the main API thread and handle failures gracefully.
*   **Action 1 (Task Queue):** Set up a Redis-backed background worker (e.g., Celery or ARQ).
*   **Action 2 (The Job):** Create a background job to generate a "Weekly Progress Report" (mock email) for the user.
*   **Action 3 (Retries & Dead-letters):** If the email service "fails", implement exponential backoff retries. If it fails 3 times, move the job to a "Dead-Letter Queue" for manual inspection.
*   **Action 4 (Idempotency):** Implement an `Idempotency-Key` header for `POST /api/daily_entry` so a user with a laggy connection doesn't accidentally log the same day twice.

### Epic 7: Testing & System Hardening
**Goal:** Prove the system works and cannot be easily broken.
*   **Action 1 (Fixtures):** Build Pytest fixtures that spin up an empty test PostgreSQL database and yield an authenticated test client.
*   **Action 2 (Failure Testing):** Write tests that deliberately send bad tokens, request non-existent commitments, and try to edit other users' data, ensuring we get the exact `401`, `404`, and `403` JSON error contracts we defined in Epic 1.
*   **Action 3 (Mocking):** Write a test for the Weekly Report background job that *mocks* the email sender so we don't actually send emails during tests.

### Epic 8: The Capstone - Bulk Import Pipeline
**Goal:** A final exam feature that forces us to use everything we've learned.
*   **The Feature:** Allow a user to upload a massive CSV file containing years of historical habit data.
*   **The Flow:** 
    1. `Auth` & `Authorization` check.
    2. API immediately returns `202 Accepted` and offloads the file to a **Background Queue**.
    3. The **Worker** parses the CSV.
    4. Database inserts are wrapped in strict **Transactions** (if one row fails, rollback all).
    5. The worker updates the user's **Redis Cache** when finished.
    6. **Structured Logging** tracks the job's progress.
    7. **Failure Scenarios to Test:** What happens if the worker crashes midway? What if the CSV has duplicate dates? What if the user hits the rate limit while uploading?
