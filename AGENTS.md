# Repository Instructions for AI Agents

## Project

This is a small FastAPI backend for serving seeded deployment event data. The service exposes deployment records, supports basic filtering, and keeps the current storage layer in memory.

## Commands

- Install dependencies: `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Run API: `fastapi dev app/main.py`
- Alternative API command: `uvicorn app.main:app --reload`
- Run tests: `pytest -q`

## Architecture

- `app/main.py`: FastAPI route definitions and HTTP error handling.
- `app/models.py`: Pydantic API models and deployment status type.
- `app/services.py`: Filtering and business logic.
- `app/repository.py`: Data access abstraction over the current in-memory dataset.
- `app/seed_data.py`: Mock deployment events.
- `tests/test_api.py`: Contract and behavior tests.

## Development Guidelines

- Keep HTTP concerns in `app/main.py`.
- Keep computation, filtering, and domain behavior in `app/services.py`.
- Add or update Pydantic models in `app/models.py` when adding response shapes.
- Keep endpoint response shapes consistent: list endpoints should return `{ "count": number, "data": [...] }`; detail endpoints should return the resource object.
- Preserve the repository boundary so storage can be swapped later without changing route code.
- Add targeted tests for new behavior or edge cases.
- Avoid broad refactors unless they directly simplify the requested change.
