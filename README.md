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
Habit tracking felt like the perfect project to start, and building it myself meant understanding the data and software behind an app.

After taking Algorithm Design I at the University of Missouri, 
I understood the fundamentals of C but I hadn't built a complex project using a clean tech stack. 
So I decided to build HabitOS, with APIs, code tests, and a real database. 
Habit tracking was a great starting point, teaching me about alembic migrations and dependency injections.

To be honest, there were parts of my code that I didn't fully understand. 
I spent hours trying to understand Alembic migrations conflicts and connect Docker with PostgreSQL.
I worked through it by using documentation on Alembic and a lot of trial and error.

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

## Project Structure (high level)

### Local Development
1. Create venv: `python -m venv .venv`
2. Activate: `source .venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --reload`

### Dependency Injection
Each request gets its own isolated database session so the code stays modular
and testable without shared state leaking between requests.

---

## Problems I Actually Ran Into

**Alembic migration conflicts** — When I changed a model schema after already
running migrations, Alembic's state and the actual database schema fell out of 
sync. I learned to treat migration history as append-only and stopped trying to 
edit existing migration files to fix mistakes.

**Docker networking** — Getting FastAPI and PostgreSQL to communicate inside 
docker-compose required understanding how to set up all of the systems to ensure that
everything was running properly. If Docker wasn't running or my connection was incorrect,
FastAPI wouldn't reach the PostgreSQL container entirely. Then I would get confusing error messages that didn't 
always address the root cause. Afterwards, I learned how to debug by testing and changing my approach.

**Understanding my own code** — The hardest problem isn't technical. SQLAlchemy 
sessions, Alembic's migration graph, and FastAPI's dependency injection system 
all have mental models that take time to internalize. I ended up copy-pasting patterns I didn't fully understand. 
Now, I've created a rule to not move forward on a new feature until I can explain the previous one clearly.
Sometimes that means sitting with confusion longer than feels comfortable.

---

## What's Next

My current priority is completing the backend with full test coverage before
starting the frontend. I want to have a solid foundation and understanding before 
adding other features.

Planned in order:

1. **Analytics endpoints** — streaks, completion rates, and date-range trend 
   queries. This is where the PostgreSQL schema design starts to pay off.
2. **Authentication** — JWT-based user accounts so the API can support multiple 
   users with isolated data.
3. **Frontend / dashboard** — A simple UI to make habit data visible and 
   interactive. The analytics layer needs to exist first for this to be 
   meaningful.
4. **ML-based recommendations** — Pattern detection on habit completion data 
   to surface insights (e.g., which habits correlate with streak success). 
   The long-term goal is using the habit data to spot behavioral patterns,
   which is what the ML recommendations are designed for.
