# HabitOS

HabitOS is a backend API for habit tracking built with FastAPI + PostgreSQL.
It supports managing habits and daily activity records (completions/check-ins),
with a service layer, Pydantic schemas, SQLAlchemy ORM models, Alembic 
migrations, and a pytest test suite.

> Status: Active development (v1).

---

## Why I Built This

I'm deeply interested in the intersection between computer science and psychology. 
Specifically in areas of self improvement and building small but compounding habits.
After taking Algorithm Design I at the University of Missouri, I understood C fundamentals but I hadn't built anything with a real tech stack. HabitOS was my way of building APIs, tests, a real database, and using project-based learning to simulate a real world setting.

---

## Tech Stack

- **Languages**: Python
- **API**: FastAPI
- **DB**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Tests**: pytest (integration-style API tests)
- **Containerization**: Docker + docker-compose

---

## Getting Started
1. Create venv: `python -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`

For Docker:
```
docker-compose up -d
```
API available at `http://localhost:8000/docs`

---

## Problems I Actually Ran Into

**Alembic migration conflicts** — When I changed a model schema after already
running migrations, Alembic's state and the actual database schema fell out of 
sync. I learned to treat migration history as append-only and stopped trying to 
edit existing migration files to fix mistakes.

**Docker networking** — Getting FastAPI and PostgreSQL to communicate inside 
docker-compose meant understanding that containers are isolated. When my connection string pointed to localhost instead of the Docker service name, FastAPI couldn't reach Postgres, and the error messages pointed to the database rather than the network configuration. I learned to trace connectivity issues from the container, rather than taking error messages at face value.

**Understanding my own code** — The hardest problem isn't technical. SQLAlchemy 
sessions, Alembic's migration graph, and FastAPI's dependency injection system 
all have mental models that take time to internalize. I ended up copy-pasting patterns I didn't fully understand. 
Now, I've created a rule to not move forward on a new feature until I can explain the previous one clearly.
Sometimes that means sitting with confusion longer than feels comfortable.

---

## What's Next

I'm currently building outward from a working backend toward a complete, deployable full-stack app.

Planned in order:

1. **Frontend / dashboard** — A simple React UI for viewing, creating, and completing habits. Making the data visible and interactive first, so every backend feature added has a user-facing impact.
2. **Authentication** — JWT-based user accounts so the API can support multiple 
   users with isolated data.
3. **Analytics endpoints** — streaks, completion rates, and date-range trend 
   queries on the dashboard.
4. **ML-based recommendations** — Pattern detection on habit completion data 
   to identify which habits correlate with streak success. The long-term goal is using the
   habit data to spot behavioral patterns, connecting to my interest in neuroscience and
   behavioral AI.
