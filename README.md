# Hexagonal Architecture in Python
This repository contains a sample Python REST API implemented according to hexagonal architecture.

## Commands

```bash
make install       # Install dependencies (requires .venv)
make format        # Format code (isort, autoflake, black)
make test          # Run all tests with pytest
make migrations    # Create alembic migration
make migrate       # Run alembic migrations
make run           # Start FastAPI server on port 8000
```

## Project Structure

```
src/sms/
├── core/           # Domain logic (business rules, independent of infrastructure)
│   ├── domain/     # Models (dataclasses) and DTOs (Pydantic)
│   ├── ports/      # Interfaces: repositories.py, services.py, unit_of_works.py
│   └── services/   # Service implementations (business logic)
├── adapters/       # Infrastructure implementations
│   ├── db/orm.py   # SQLAlchemy Data Mapper (imperative mapping)
│   ├── repositories/  # Repository implementations
│   ├── unit_of_works.py  # UoW implementations with AsyncSession
│   └── entry_points/api/  # FastAPI endpoints
└── config/
    ├── containers.py  # dependency-injector DI container
    └── settings.py    # Database and app configuration
```

## Key Patterns

- **SQLAlchemy Data Mapper Pattern**: Tables are defined separately from domain models (dataclasses) and mapped imperatively in `orm.py`. Domain models remain free of ORM dependencies.
- **Dependency Injection**: Uses `dependency-injector` library to decouple core business logic from infrastructure code. This makes the core logic independent of external systems, which can be easily swapped or modified without affecting the core.
- **Unit of Work**: Transaction management via async context managers.
- **Soft Deletes**: All entities have `deleted_at` field for logical deletion.
- **Fakes for Testing**: In-memory fake implementations of repositories in `adapters/repositories/fakes/` for unit testing services without a database.

## Database

- PostgreSQL with asyncpg driver
- Production: port 5435, Test: port 5436
- Alembic for migrations
