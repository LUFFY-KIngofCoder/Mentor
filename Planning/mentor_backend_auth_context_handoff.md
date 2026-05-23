# Mentor Backend Engineering Context Handoff

## Current Goal
Building Mentor as:
- a behavioral accountability system
- backend-first architecture
- production-style engineering learning project

Main learning focus:
- backend engineering
- systems thinking
- auth architecture
- database design
- API architecture
- later AI engineering

---

# Current Backend Stack

Backend:
- FastAPI

Database:
- PostgreSQL

ORM:
- SQLAlchemy

Validation:
- Pydantic

Migrations:
- Alembic

Authentication:
- JWT
- passlib
- bcrypt
- python-jose

---

# Current Folder Structure

```text
Backend/
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schema/
│   ├── services/
│   ├── utils/
│   ├── __init__.py
│   └── main.py
├── .env
├── alembic.ini
└── venv/
```

---

# Exact Backend State (Current Working State)

This section documents EXACTLY what currently exists in the backend.

---

# Current Working Routes

## Root Route

```python
GET /
```

Purpose:
- backend health check
- verify FastAPI server running

Returns:

```json
{
  "message": "Mentor Backend Running"
}
```

---

# User Routes

## Create User

```python
POST /users
```

Current behavior:
- accepts user registration data
- hashes password before storing
- stores user in PostgreSQL
- returns created user

Current schema used:

```python
UserCreate
```

Expected fields:

```json
{
  "name": "...",
  "email": "...",
  "password": "..."
}
```

Important implementation details:
- password is hashed using bcrypt/passlib
- raw password NEVER stored
- UUID generated automatically
- created_at generated automatically

Response model:

```python
UserResponse
```

---

## Get User By ID

```python
GET /users/{user_id}
```

Current behavior:
- fetches user using UUID
- queries PostgreSQL using SQLAlchemy
- returns matching user

Concepts practiced:
- path parameters
- UUID usage
- SQLAlchemy query filtering
- response models

---

# Authentication Routes

## Login Route

```python
POST /auth/login
```

IMPORTANT:
Current function name is:

```python
login
```

NOT:

```python
login_user
```

Current behavior:
- verifies email exists
- verifies hashed password
- generates JWT token
- returns access token

Current login flow:

```text
email/password
↓
find user in DB
↓
verify_password()
↓
create_access_token()
↓
return JWT
```

Current JWT payload:

```python
{"sub": str(user.id)}
```

Current response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

# Current Working Database Dependencies

## get_db()

Location:

```text
app/db/session.py
```

Purpose:
- creates SQLAlchemy DB session
- yields DB session
- closes session automatically

Current understanding:

```python
db: Session = Depends(get_db)
```

means:

```text
FastAPI automatically creates and injects DB session
```

---

# Current Working Security Functions

Location:

```text
app/core/security.py
```

Current implemented functions:

## hash_password()

Purpose:
- converts plain password into secure hash

Uses:
- passlib
- bcrypt

---

## verify_password()

Purpose:
- compares plain password against stored hash

Important understanding:
- hashes are NOT decrypted
- input password is hashed again and compared

---

## create_access_token()

Purpose:
- creates JWT token
- embeds expiry
- signs token cryptographically

Current JWT fields:

```python
sub
exp
```

Uses:
- python-jose

---

# Current Working Config System

Location:

```text
app/core/config.py
```

Current variables:

```python
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

Loaded from:

```text
.env
```

Important debugging lesson learned:
- typo in SECRET_KEY caused JWT failure

---

# Current Working Time Utility

Location:

```text
app/utils/time.py
```

Current timezone decision:

```text
Asia/Kolkata (IST)
```

Current helper:

```python
now_ist()
```

Purpose:
- centralized app time handling
- future streak/date consistency

---

# Current Database Model State

## User Model

Current fields:

```text
id
name
email
password_hash
created_at
updated_at
```

Important architecture lesson:
- SQLAlchemy models use SQLAlchemy types
- Pydantic types belong ONLY in schemas

Correct implementation:

```python
email = Column(String)
```

NOT:

```python
email = Column(EmailStr)
```

---

# Current Pydantic Schemas

Location:

```text
app/schema/user.py
```

Current schemas:

## UserCreate

Used for:
- registration input

Fields:

```text
name
email
password
```

---

## UserResponse

Used for:
- API responses

Fields:

```text
id
name
email
created_at
```

Uses:

```python
from_attributes = True
```

---

## UserLogin

Used for:
- login requests

Fields:

```text
email
password
```

---

# Current Auth Architecture Understanding

Current understanding of future auth pipeline:

```text
Request
↓
Bearer token extracted
↓
JWT decoded
↓
Signature verified
↓
Expiry checked
↓
user_id extracted
↓
DB user fetched
↓
Authenticated user injected into route
```

Current next implementation target:

```text
get_current_user()
```

---

# Current Working Packages

Currently installed/used:

```text
fastapi
uvicorn
sqlalchemy
psycopg2
alembic
pydantic
python-dotenv
passlib
bcrypt==4.0.1
python-jose
pytz
```

---

# Important Bugs Already Solved

## Bug 1 — Wrong SQLAlchemy Email Type

Wrong:

```python
Column(EmailStr)
```

Correct:

```python
Column(String)
```

Concept learned:
- schema responsibility vs DB responsibility

---

## Bug 2 — Raw Password Storage

Initially:

```python
password_hash=user.password
```

Fixed using:

```python
hash_password()
```

---

## Bug 3 — Wrong SQLAlchemy Query

Wrong:

```python
db.query(user_id)
```

Correct:

```python
db.query(User)
```

Concept learned:
- SQLAlchemy queries models/tables

---

## Bug 4 — bcrypt Compatibility Issue

Issue:
- passlib/bcrypt mismatch
- misleading 72-byte password error

Fix:

```bash
pip install bcrypt==4.0.1
```

Major lesson:
- symptoms vs root causes
- dependency debugging

---

## Bug 5 — SECRET_KEY Config Typo

Issue:
- JWT failing
- SECRET_KEY loading as None

Cause:
- typo in config variable

Concept learned:
- env/config debugging

---

# What Has Been Built So Far

## FastAPI App

main.py currently:
- initializes FastAPI app
- includes user router
- has root health endpoint

---

# Database Setup

Completed:
- PostgreSQL connection
- SQLAlchemy engine
- SessionLocal
- Base declarative setup
- get_db dependency
- Alembic migrations working

---

# User Model Built

User table currently contains:

```text
id (UUID)
name
email
password_hash
created_at
updated_at
```

Important fix learned:
- SQLAlchemy models should use SQLAlchemy column types
- Pydantic types like EmailStr should ONLY exist in schemas

Correct:

```python
email = Column(String, unique=True, index=True, nullable=False)
```

NOT:

```python
email = Column(EmailStr)
```

---

# User Schemas Built

Current schemas:

```text
UserCreate
UserResponse
UserLogin
```

Concept learned:
- separate DB models from request/response schemas

---

# Password Hashing Implemented

Created:

```text
app/core/security.py
```

Implemented:
- hash_password()
- verify_password()

Concepts learned:
- hashing is one-way
- hashing != encryption
- passwords should NEVER be stored raw
- systems assume DB leaks can happen

---

# Authentication System Built

Implemented:

```text
POST /auth/login
```

Flow:

```text
email/password
↓
verify user exists
↓
verify password hash
↓
generate JWT token
↓
return access_token
```

JWT payload currently stores:

```python
{"sub": str(user.id)}
```

Concept learned:
- JWT is signed identity proof
- JWT is NOT encryption
- stateless authentication
- token expiry exists to reduce security risk

---

# JWT Setup

Implemented:

```text
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

inside:

```text
app/core/config.py
```

---

# Timezone Decision

Mentor currently uses:

```text
Asia/Kolkata (IST)
```

Created:

```text
app/utils/time.py
```

with:

```python
now_ist()
```

Concept learned:
- time is business logic in Mentor
- later production systems usually store UTC internally

---

# Major Debugging Lessons Learned

## 1. bcrypt/passlib Dependency Issue

Problem:
- bcrypt compatibility mismatch
- misleading 72-byte password error

Fix:

```bash
pip install bcrypt==4.0.1
```

Concepts learned:
- dependency mismatches
- root cause vs symptom
- traceback reading
- environment debugging
- pinned dependency versions

Important insight:
- error messages are clues, not absolute truth

---

## 2. Config Debugging

Issue:
- SECRET_KEY typo in config
- JWT encode failing

Concepts learned:
- env variable loading
- config debugging
- import timing
- system input validation

---

# Current Auth Architecture Understanding

Mentor auth flow:

```text
Register
↓
Hash password
↓
Store user
↓
Login
↓
Verify hash
↓
Generate JWT
↓
Frontend stores token
↓
Protected routes use token
```

---

# Concepts Learned Deeply

## Authentication vs Authorization

Authentication:

```text
Who are you?
```

Authorization:

```text
What are you allowed to do?
```

Important insight:
- many backend security failures are authorization failures
- ownership validation will matter later

---

# Dependency Injection Understanding

Learned:

```python
db: Session = Depends(get_db)
```

means:

```text
FastAPI executes dependency and injects result automatically
```

Important concept:
- routes declare WHAT they need
- framework manages HOW dependencies are built

---

# Current `get_current_user()` Progress

Started learning:

```text
OAuth2PasswordBearer
get_current_user()
protected routes
```

Current understanding:

```text
Request
↓
Extract bearer token
↓
Decode JWT
↓
Verify signature
↓
Check expiry
↓
Extract user_id
↓
Fetch user from DB
↓
Inject authenticated user
```

Important understanding:
- OAuth2PasswordBearer ONLY extracts token
- it does NOT authenticate user itself

---

# Important Current Clarification

Current login route function name is:

```python
login
```

NOT:

```python
login_user
```

Need to maintain accurate context moving forward.

---

# Current Learning Style Preference

Important:
- too much theory kills momentum
- implementation + reasoning together works best
- shorter theory blocks
- practical building while understanding concepts

Teaching style should be:
- explain WHY briefly
- immediately implement
- debug together
- reason through errors together

NOT:
- endless theory before coding

---

# Immediate Next Step

Continue implementing:

```text
get_current_user()
```

Goals:
- protected routes
- token decoding
- authenticated user injection
- `/auth/me`
- understanding dependency injection pipeline

Likely next concepts:
- OAuth2PasswordBearer
- Depends chaining
- protected endpoints
- current user injection
- ownership validation

---

# Long-Term Mentor Roadmap

Current roadmap focus:

## Phase 1
- auth
- commitments
- daily entries
- validation logic

## Phase 2
- dashboard
- analytics
- streaks

## Phase 3
- temporal integrity
- missed day system

## Phase 4
- AI weekly review system

Important restriction:
- DO NOT touch advanced AI orchestration yet
- no LangGraph
- no agents
- no vector DBs yet

Current priority remains:

```text
strong backend engineering fundamentals
```

---

# Most Important Engineering Lessons So Far

## 1.
Error messages are evidence, not absolute truth.

## 2.
Root cause analysis matters more than patching symptoms.

## 3.
Large systems fail across layers:
- app
- dependency
- config
- infra
- environment

## 4.
Strong engineering requires:
- debugging discipline
- architecture thinking
- understanding responsibility boundaries

## 5.
Mentor is not just a startup project.
It is an engineering training ground.

