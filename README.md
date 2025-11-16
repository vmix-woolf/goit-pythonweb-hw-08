# Проєкт зі створення REST API для управління контактами.

## Technology stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Alembic
- Pydantic v2
- Docker

## Installation and launch
Install dependencies:
```poetry install```

Launch PostgreSQL via Docker:
```docker compose up -d```

Apply Alembic migrations:
```alembic upgrade head```

Launch the server:
```uvicorn app.main:app --reload```

API available at:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

## Project structure

```
app
├── main.py
├── database.py
├── config.py
│
├── models
│   └── contact.py
│
├── schemas
│   └── contact.py
│
├── crud
│   └── contact.py
│
└── api
    └── contacts.py
```


## API functionality
POST /contacts — create a contact

GET /contacts — list of contacts

GET /contacts/{id} — get a contact

PUT /contacts/{id} — update a contact

DELETE /contacts/{id} — delete a contact

GET /contacts/search — search by first name, last name, email

GET /contacts/birthdays — birthdays in the next 7 days

## Alembic
Create migration:
```alembic revision --autogenerate -m “message”```

Apply migrations:
```alembic upgrade head```
