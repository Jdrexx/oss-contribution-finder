# Open Source Contribution Finder

![Python](https://img.shields.io/badge/Python-3.11_|_3.12-3776AB?style=flat-square&logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite) ![GitHub API](https://img.shields.io/badge/GitHub_API-181717?style=flat-square&logo=github) ![Beginner Friendly](https://img.shields.io/badge/Beginner_Friendly-22C55E?style=flat-square)

Search GitHub issues by skill, filter by difficulty, and find your first open-source contribution.

## Features
- Search GitHub issues by skill keywords
- Filter by language and difficulty
- Estimated time-to-fix indicator
- Bookmark interesting issues
- GitHub API integration

## Quick Start

```bash
uv sync
uv run uvicorn src.main:app --reload --port 8107
```

Open: http://localhost:8107

## API
- `GET /` - browser demo
- `GET /api/health` - health check
- `GET /docs` - interactive FastAPI docs

## Verify
```bash
uv run pytest -q
```
