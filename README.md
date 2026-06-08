# Open Source Contribution Finder

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
