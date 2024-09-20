# Hexagonal Architecture in Python
This repository contains a sample Python REST API implemented according to hexagonal architecture.


### Project Structure
```
project_dir/
├── src/
│   ├── sms/
│   │   ├── adapters/
│   │   │   ├── db/
│   │   │   │   ├── migrations/
│   │   │   │   │   └── versions/
│   │   │   │   │       └── a15200892d2f_add_product_permissions.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── orm.py
│   │   │   ├── entry_points/
│   │   │   │   ├── api/
│   │   │   │   │   ├── v1/
│   │   │   │   │   │   └── brand.py
│   │   │   │   │   ├── app.py
│   │   │   │   │   ├── base.py
│   │   │   │   │   └── main.py
│   │   │   │   └── __init__.py
│   │   │   ├── repositories/
│   │   │   │   │── brand.py
│   │   │   │   └── __init__.py
│   │   │   ├── unit_of_works.py
│   │   │   └── __init__.py
│   │   ├── config/
│   │   │   ├── containers.py
│   │   │   └── settings.py
│   │   ├── core/
│   │   │   ├── domain/
│   │   │   │   ├── dtos.py
│   │   │   │   ├── models.py
│   │   │   │   └── __init__.py
│   │   │   ├── ports/
│   │   │   │   ├── repositories.py
│   │   │   │   ├── services.py
│   │   │   │   ├── unit_of_works.py
│   │   │   │   └── __init__.py
│   │   │   ├── services/
│   │   │   │   ├── brand_service_impl.py
│   │   │   │   └── __init__.py
│   │   │   ├── helpers.py
│   │   │   ├── constants.py
│   │   │   └── __init__.py
│   │   └── __init__.py
├── tests/
│   └── __init__.py
├── .gitignore
├── requirements.txt
├── alembic.ini
└── README.md
```
`src/` Contains the source code of the project
- `sms/` Main application directory
  - `adapters/` Contains the implementations of the adapters (e.g. database, API, etc.)
    - `db/` Database related code (e.g. ORM, migrations, etc.)
    - `entry_points/` Entry points of the application, in this project we use just FastAPI
  - `config/` Configuration files like `settings.py` for database connection and `containers.py` for dependency injection
  - `core/` Core domain logic
     - `domain/` Domain models and DTOs
     - `ports/` Interfaces or abstract classes for the core domain.
     - `services/` Service implementations
     - `helpers.py` Helper functions and utilities
     - `constants.py` Constant values used across the application

#### Key packages used
- **SQLAlchemy**: The way SQLAlchemy is implemented in this project is called the **Data Mapper Pattern**. This pattern is characterized by the use of a separate layer of mappers that move data between objects and a database while keeping them independent of each other.  
- **dependency-injector for Dependency Injection:** DI helps in decoupling the core business logic from the infrastructure code. This makes the core logic independent of external systems, which can be easily swapped or modified without affecting the core. 
