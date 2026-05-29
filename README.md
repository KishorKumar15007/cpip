# CP Intelligence Platform

A personal competitive programming analytics platform that aggregates problem-solving data from Codeforces and LeetCode and provides insights into learning progress, problem-solving patterns, and performance trends.

## Goals

- Track competitive programming activity across multiple platforms
- Build a unified database of problems, submissions, and user statistics
- Analyze performance trends over time
- Identify strengths and weak areas across algorithmic topics
- Serve as a long-term learning and engineering project

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic

### Infrastructure
- Redis
- Celery
- Docker

## Current Status

🚧 Phase 1: Data Layer

Planned features:

- PostgreSQL schema design
- Codeforces data synchronization
- LeetCode data synchronization
- Background job processing with Celery
- REST API endpoints
- Authentication
- Database migrations

## Repository Structure

```
backend/        Application code
db/             Schema, queries, and database assets
docs/           Architecture notes and decisions
infrastructure/ Deployment and infrastructure files
local/          Local-only files (ignored by Git)
```

## Purpose

This project is primarily a systems and backend engineering exercise built around a real workflow: competitive programming practice. The platform is intended to grow incrementally, with each phase focusing on a specific engineering domain while remaining useful as a personal tool.

## License

MIT
