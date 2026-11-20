# Datheon Python + FastAPI Backend Development Internship
### Official Technical Repository • Application ID: `DT-2026-89H4F`

**Candidate Name:** Syed Jawad Hussain Shah  
**Program Track:** Python + FastAPI Backend Development Internship (4-Week Engineering Cohort)  
**Verification Portal:** [https://www.datheon.in/verify?id=DT-2026-89H4F](https://www.datheon.in/verify?id=DT-2026-89H4F)  
**Registered Email:** `syedjawadoffical@gmail.com`

---

## 📌 Executive Summary
This repository contains the complete, production-tested deliverables for all four milestones of the **Datheon Python + FastAPI Backend Development Internship**. Each task adheres to enterprise-grade asynchronous patterns, PEP 484 type hints, Pydantic v2 schemas, cryptographic JWT security, SQLAlchemy ORM persistence, and containerized microservice design.

```
Datheon_Python_FastAPI_Backend_Internship/
├── Task_1_BookStore_REST_API/
│   ├── main.py                  # Full asynchronous CRUD REST API with Pydantic validation
│   ├── test_task1.py            # Automated test suite (Status codes 200, 201, 204, 404, 422)
│   └── Task1_BookStore_REST_API.ipynb
├── Task_2_User_Authentication_JWT_RBAC/
│   ├── main.py                  # Bcrypt hashing, signed JWT token issuance, OAuth2 & RBAC
│   ├── test_task2.py            # Authentication & role-based permission test suite
│   └── Task2_User_Authentication_JWT_RBAC.ipynb
├── Task_3_Database_Persistence_SQLAlchemy/
│   ├── database.py              # SQLite & SQLAlchemy declarative engine & sessionmaker
│   ├── models.py                # Relational ORM models with Foreign Keys & User->Notes relationship
│   ├── schemas.py               # Pydantic v2 DTOs with from_attributes=True
│   ├── crud.py                  # CRUD operations & relational join query functions
│   ├── main.py                  # FastAPI server with Depends(get_db) dependency injection
│   ├── test_task3.py            # Persistence & foreign key relational test suite
│   └── Task3_Database_Persistence_SQLAlchemy.ipynb
├── Task_4_Microservice_BackgroundTasks_Docker/
│   ├── main.py                  # Microservice with async BackgroundTasks & rate limiting
│   ├── Dockerfile               # Multi-stage production container build with healthcheck
│   ├── docker-compose.yml       # Production orchestration
│   ├── requirements.txt         # Pinned production dependencies
│   ├── test_task4.py            # Test suite for async queues and rate limiting
│   └── Task4_Microservice_BackgroundTasks_Docker.ipynb
└── README.md
```

---

## 🚀 Tasks Breakdown & Deliverables

### Task 1: BookStore REST API with Pydantic Validation
* **Features:** Asynchronous CRUD operations with strict Pydantic v2 data models, input sanitization, and auto-generated Swagger UI (`/docs`).
* **Endpoints:** `GET /books` (query filters: genre, author, min/max price, pagination), `POST /books` (201 Created), `GET /books/{id}`, `PUT /books/{id}`, `DELETE /books/{id}` (204 No Content).
* **Validation:** Custom price, year, and stock constraints with automatic `422 Unprocessable Entity` error responses.

### Task 2: User Authentication & RBAC with JWT
* **Security:** `passlib` with `bcrypt` password hashing and `python-jose` for signed JWT token creation and validation (`HS256`).
* **Role-Based Access Control:** Separate permissions for `user` and `admin` roles.
* **Endpoints:** `POST /auth/register`, `POST /auth/login` (OAuth2 Password flow), `GET /users/me` (Protected), `GET /admin/dashboard` (403 Forbidden for non-admins).

### Task 3: Database Persistence with SQLAlchemy & SQLite
* **Architecture:** Enterprise 3-tier structure (`database.py`, `models.py`, `schemas.py`, `crud.py`, `main.py`).
* **Relational Schema:** `User` has a one-to-many relationship with `Note` via foreign key `user_id`.
* **Dependency Injection:** Database sessions are scoped per request using `Depends(get_db)`.

### Task 4: Microservice with Background Tasks & Docker
* **Asynchronous Jobs:** Decoupled background task queues for email notifications and webhook dispatches using `FastAPI.BackgroundTasks`.
* **Rate Limiting:** Sliding window rate limiter enforcing max requests window per client IP.
* **Containerization:** Multi-stage production `Dockerfile` with automated container health check (`GET /health`).

---

## 🛠️ Verification & Test Suite Execution

All four tasks have been thoroughly verified with automated test suites:

```bash
# Task 1 Test
python Task_1_BookStore_REST_API/test_task1.py

# Task 2 Test
python Task_2_User_Authentication_JWT_RBAC/test_task2.py

# Task 3 Test
python Task_3_Database_Persistence_SQLAlchemy/test_task3.py

# Task 4 Test
python Task_4_Microservice_BackgroundTasks_Docker/test_task4.py
```

---

## 📜 Candidate Declaration
I, **Syed Jawad Hussain Shah**, hereby declare that the implementations provided in this repository are my authentic technical work submitted to the **Datheon Academic & Technical Directorate** under Application ID **`DT-2026-89H4F`**.
