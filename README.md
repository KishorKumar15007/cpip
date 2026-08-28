# CP Intelligence Platform

A personal competitive programming analytics platform that aggregates problem-solving data from Codeforces and LeetCode into a unified system for analyzing learning progress, performance, and problem-solving patterns.

## Features

- Codeforces and LeetCode data synchronization
- Unified problems, submissions, tags, and contest history
- Incremental synchronization with duplicate-safe ingestion
- Background synchronization using Celery and Redis
- REST API built with FastAPI
- JWT authentication with access and refresh tokens
- PostgreSQL persistence using SQLAlchemy
- Database migrations using Alembic

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Celery

## Getting Started

### Prerequisites

- Python
- PostgreSQL
- Redis

### Installation

Clone the repository and create a virtual environment:

```bash
git clone 
cd CPIP

python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file from `.env.example` and configure the required database, Redis, and authentication settings.

Run the database migrations:

```bash
alembic upgrade head
```

### Running

Start the FastAPI application:

```bash
uvicorn backend.main:app --reload
```

Start the Celery worker separately:

```bash
celery -A backend.celery_app worker --loglevel=info
```

The API documentation is available through FastAPI's generated documentation at:

```text
http://localhost:8000/docs
```

## Configuration

Configuration is provided through environment variables. See `.env.example` for the required variables.
