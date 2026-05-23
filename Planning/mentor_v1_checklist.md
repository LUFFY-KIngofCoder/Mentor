# Mentor — Version 1 Checklist

## Behavioral Accountability & Execution System

---

# VERSION 1 OBJECTIVE

Mentor V1 is a behavioral accountability system designed to:

- detect behavioral drift
- increase self-awareness
- improve consistency
- create honest execution tracking
- reduce self-deception

This is NOT:
- a productivity app
- a motivational app
- an AI therapist
- a dopamine tracker

The system should function as:
a behavioral mirror.

---

# CORE PRODUCT LOOP

```text
Day 0 Commitment
        ↓
Daily Check-In
        ↓
Behavior Logging
        ↓
Missed Day Detection
        ↓
Forced Reflection
        ↓
Weekly AI Review
        ↓
Behavioral Awareness
```

---

# VERSION 1 SUCCESS CRITERIA

Mentor V1 succeeds if:

- users consistently log entries
- missed days become visible
- behavioral patterns become obvious
- weekly reviews create awareness
- users become more honest about execution

---

# SECTION 1 — DAY 0 COMMITMENT SYSTEM

## Goal

Create behavioral commitments that cannot be renegotiated daily.

---

# Features

## Commitment Creation

User defines:
- improvement areas
- metrics to track
- commitment duration

---

## Commitment Rules

- minimum duration: 30 days
- cannot instantly cancel
- daily tracking required

---

# Example Metrics

- sleep hours
- deep work hours
- distractions
- smoking count
- gym/workout
- study hours
- screen time
- mood
- energy

---

# Backend Tasks

- [ ] Create Commitment model
- [ ] Create TrackingMetric model
- [ ] Create commitment APIs
- [ ] Add duration validation
- [ ] Add commitment status logic

---

# Frontend Tasks

- [ ] Build onboarding page
- [ ] Build metric selection UI
- [ ] Build duration selector
- [ ] Build commitment summary screen

---

# SECTION 2 — DAILY CHECK-IN SYSTEM

## Goal

Build the core behavioral logging workflow.

This is the HEART of the product.

---

# Daily Input Fields

## Quantitative

- sleep hours
- deep work hours
- distraction hours
- smoking count
- exercise completed

---

## Qualitative

- what you avoided today
- biggest win
- biggest failure
- emotional state
- short journal entry

---

# Daily Rules

- only one entry per day
- no backfilling missed days
- entries lock after day ends
- missed days auto-detected

---

# Backend Tasks

- [ ] Create DailyEntry model
- [ ] Create CRUD APIs
- [ ] Prevent duplicate entries
- [ ] Add date locking logic
- [ ] Auto-associate logged-in user

---

# Frontend Tasks

- [ ] Build daily check-in form
- [ ] Add validation
- [ ] Add submission flow
- [ ] Add loading states
- [ ] Add success/error handling

---

# SECTION 3 — MISSED DAY SYSTEM

## Goal

Force behavioral honesty.

---

# Rules

If user misses a day:
- day is permanently marked missed
- no retroactive editing
- next login forces reflection

---

# Reflection Questions

- Why did you miss the day?
- What caused the drift?
- What were you avoiding?
- What disrupted execution?

---

# Backend Tasks

- [ ] Create MissedDayReflection model
- [ ] Add missed-day detector
- [ ] Add reflection APIs
- [ ] Add temporal lock logic

---

# Frontend Tasks

- [ ] Build missed-day modal
- [ ] Build reflection form
- [ ] Add missed timeline indicators

---

# SECTION 4 — DASHBOARD SYSTEM

## Goal

Create operational visibility into behavior.

---

# Dashboard Must Show

- streak count
- missed days
- consistency score
- recent entries
- weekly trends
- completion history

---

# Charts

- deep work trends
- sleep trends
- distraction trends
- consistency trends

---

# Backend Tasks

- [ ] Create dashboard APIs
- [ ] Build trend calculations
- [ ] Build streak calculations
- [ ] Build consistency score logic

---

# Frontend Tasks

- [ ] Build dashboard layout
- [ ] Add charts
- [ ] Add timeline/history
- [ ] Add trend cards

---

# SECTION 5 — WEEKLY AI REVIEW SYSTEM

## Goal

Generate behavioral awareness through pattern analysis.

---

# AI SHOULD:

- detect patterns
- identify correlations
- expose drift
- summarize behavioral trends

---

# AI SHOULD NOT:

- emotionally manipulate
- act like therapist
- give fake motivation
- pretend to diagnose psychology

---

# Example Insights

```text
Your low-focus days correlate with poor sleep.

You consistently avoid difficult work late at night.

Distraction-heavy days reduce deep work significantly.

Your best execution days follow structured mornings.
```

---

# Weekly Review Includes

- consistency analysis
- behavioral trends
- drift patterns
- missed-day analysis
- reflection summaries

---

# Backend Tasks

- [ ] Create AI analysis service
- [ ] Create weekly aggregation logic
- [ ] Build insight generation workflow
- [ ] Store weekly reviews

---

# Frontend Tasks

- [ ] Build weekly review page
- [ ] Build insight cards
- [ ] Add trend summaries
- [ ] Add review history

---

# SECTION 6 — DATABASE DESIGN

## Core Tables

---

# User

```text
id
email
username
password_hash
created_at
```

---

# Commitment

```text
id
user_id
title
duration_days
start_date
end_date
status
created_at
```

---

# TrackingMetric

```text
id
commitment_id
metric_name
metric_type
target_value
```

---

# DailyEntry

```text
id
user_id
date
sleep_hours
deep_work_hours
distraction_hours
mood_score
energy_score
journal_entry
what_avoided
biggest_win
biggest_failure
created_at
```

---

# MissedDayReflection

```text
id
user_id
missed_date
reason
reflection
created_at
```

---

# WeeklyReview

```text
id
user_id
week_start
summary
patterns
risk_signals
recommendations
created_at
```

---

# SECTION 7 — BACKEND ARCHITECTURE

## Stack

Backend:
- FastAPI

Database:
- PostgreSQL

ORM:
- SQLAlchemy

Validation:
- Pydantic

---

# Backend Structure

```text
backend/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
├── analytics/
├── ai/
├── auth/
├── utils/
└── main.py
```

---

# SECTION 8 — DEVELOPMENT ORDER

## STEP 1

Build:
- database
- DailyEntry model
- CRUD APIs
- frontend form

NO AI YET.

---

## STEP 2

Build:
- dashboard
- streak logic
- trend calculations
- missed-day system

---

## STEP 3

Use Mentor daily for:
- 7–14 days minimum

Observe:
- friction
- emotional resistance
- missing workflows
- usage behavior

---

## STEP 4

ONLY THEN:
add weekly AI reviews.

---

# SECTION 9 — VERSION 1 RESTRICTIONS

DO NOT BUILD:

- social features
- teams
- public accountability
- voice assistants
- autonomous agents
- emotion prediction
- wearables
- gamification systems
- reward systems
- advanced analytics

---

# FINAL RULE

Mentor V1 must become:
a system you genuinely use daily.

If you stop using it:
the workflow is wrong.
