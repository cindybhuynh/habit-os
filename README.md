# HabitOS 

HabitOS is a backend API for habit tracking built with FastAPI + PostgreSQL.  
It supports managing habits and related daily activity records (e.g., completions/check-ins), with a service layer, Pydantic schemas, SQLAlchemy ORM models, Alembic migrations, and a pytest test suite.

> Status: Active development (v1).  
> Goal: Learn real backend fundamentals (DI/session lifecycle, transactions, ORM ↔ schema serialization, migrations, testing).

---

## Tech Stack

- **API**: FastAPI
- **DB**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Tests**: pytest (integration-style API tests)
- **Containerization**: Docker + docker-compose

---

## Project Structure (high level)
### Dependency Injection
Each request to the database gets its own isolated database connection so that the code remains modular and easier to test.
