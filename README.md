# Access Cloud Prototype

This repository contains a minimal FastAPI-based prototype that demonstrates
basic CRUD operations for records. It is **not** a full MS Access replacement
but serves as a starting point for development using TDD.

## Requirements

- Python 3.11+
- `fastapi`
- `uvicorn`
- `sqlmodel`
- `pytest`

Install dependencies:

```bash
pip install fastapi uvicorn sqlmodel pytest
```

## Running the App

```bash
uvicorn app.main:app --reload
```

## Running Tests

```bash
pytest
```
