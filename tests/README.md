# Backend Tests

This directory contains backend tests for the FastAPI application in `src/app.py`.

## Run tests

From the repository root:

```bash
git clone <repo>
cd skills-getting-started-with-github-copilot
pytest
```

## Test setup

- `pytest` is required and is listed in `requirements.txt`
- The tests use `fastapi.testclient.TestClient` to exercise the FastAPI app
- Test files are organized under `tests/` to keep backend test code separate from app source

## Coverage

The current test suite covers:

- root redirect behavior
- activity listing retrieval
- signup and unregister routes
- error handling for duplicates, missing activities, and missing participants
