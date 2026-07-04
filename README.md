# Open Source Contribution Finder

![Python](https://img.shields.io/badge/Python-3.11_%7C_3.12-3776AB?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite)

Search GitHub issues by skill keyword, filter by language and difficulty, and find your first open-source contribution. Bookmarks issues for later and estimates time-to-fix based on labels and conversation length.

## Features

- Search GitHub issues by skill keywords (e.g. "python", "javascript", "documentation")
- Filter by language, label, and difficulty level
- Estimated time-to-fix indicator based on issue metadata
- Bookmark interesting issues for later reference
- Paginated results from the GitHub API

## Quick Start

```bash
uv sync
uv run uvicorn src.main:app --reload --port 8107
```

Open: http://localhost:8107

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Browser demo UI |
| GET | `/api/health` | Health check |
| GET | `/docs` | Interactive API docs |

## Tests

```bash
uv run pytest -q
```
