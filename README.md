# Deployment API

Small backend service for serving seeded deployment event data.

## What It Does

- Serves 45 mock deployment events across multiple services and statuses in May 2026.
- Lists deployments with optional `service` and `status` filters.
- Fetches a single deployment by ID.
- Keeps storage in memory behind a small repository boundary.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```bash
fastapi dev app/main.py
```

API: `http://127.0.0.1:8000`
Docs: `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Path | Notes |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `GET` | `/deployments` | Supports `service` and `status` query filters |
| `GET` | `/deployments/{deployment_id}` | Returns `404` when the deployment does not exist |

Example:

```bash
curl "http://127.0.0.1:8000/deployments?service=billing-api&status=failed"
```

## Run tests

```bash
pytest -q
```

## Structure

```text
app/main.py        FastAPI routes and HTTP errors
app/models.py      Pydantic API models
app/services.py    Filtering and business logic
app/repository.py  Data access wrapper
app/seed_data.py   Mock deployment events
tests/test_api.py  API contract tests
```
