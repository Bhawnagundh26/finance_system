# Finance Tracking System

A REST API backend built with Django, Django REST Framework, and SQLite.

## Tech Stack
- Python 3.10+
- Django 5.x
- Django REST Framework
- Simple JWT (authentication)
- SQLite (database)

## Setup Instructions

### 1. Clone the repository
git clone <your-repo-url>
cd finance_system

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run migrations
python manage.py makemigrations users
python manage.py makemigrations transactions
python manage.py migrate

### 5. Seed sample data
python seed.py

### 6. Start the server
python manage.py runserver

### 7. Run tests
python manage.py test tests

## API Endpoints

| Method | URL                            | Access         | Description          |
|--------|--------------------------------|----------------|----------------------|
| POST   | /api/auth/register/            | Public         | Register new user    |
| POST   | /api/auth/login/               | Public         | Get JWT token        |
| POST   | /api/auth/token/refresh/       | Public         | Refresh access token |
| GET    | /api/auth/me/                  | Any logged in  | View own profile     |
| GET    | /api/auth/list/                | Admin only     | List all users       |
| GET    | /api/transactions/             | Any logged in  | List transactions    |
| POST   | /api/transactions/             | Admin only     | Create transaction   |
| GET    | /api/transactions/<id>/        | Any logged in  | Get one transaction  |
| PATCH  | /api/transactions/<id>/        | Admin only     | Update transaction   |
| DELETE | /api/transactions/<id>/        | Admin only     | Delete transaction   |
| GET    | /api/transactions/summary/     | Admin/Analyst  | Financial summary    |
| GET    | /admin/                        | Superuser      | Django admin panel   |

## Filtering Transactions

GET /api/transactions/?type=income
GET /api/transactions/?category=Salary
GET /api/transactions/?start_date=2024-01-01&end_date=2024-03-31
GET /api/transactions/?page=1&page_size=5

## Roles & Permissions

| Feature                  | Viewer | Analyst | Admin |
|--------------------------|--------|---------|-------|
| View own transactions    | Yes    | Yes     | Yes   |
| View all transactions    | No     | Yes     | Yes   |
| Create transaction       | No     | No      | Yes   |
| Update transaction       | No     | No      | Yes   |
| Delete transaction       | No     | No      | Yes   |
| View summary/analytics   | No     | Yes     | Yes   |
| View all users           | No     | No      | Yes   |

## Test Credentials (after running seed.py)

| Username | Password   | Role    |
|----------|------------|---------|
| admin    | admin123   | admin   |
| analyst  | analyst123 | analyst |
| viewer   | viewer123  | viewer  |

## Authentication

All protected endpoints require a Bearer token in the header:
Authorization: Bearer <your_access_token>

Get your token by calling POST /api/auth/login/ with username and password.

## Assumptions Made

- Viewers can only see their own transactions; Analysts and Admins see all
- Only Admins can create, update, or delete transactions
- Amount must be greater than zero (validated at serializer level)
- Category cannot be blank (validated at serializer level)
- SQLite used for simplicity as this is an assessment project
- JWT access token expires in 1 hour; refresh token in 1 day

## Project Structure

finance_system/         - Django project config (settings, urls)
transactions/           - Transactions app (models, views, serializers, services)
users/                  - Users app (custom user model, auth, roles)
tests/                  - Automated test cases
seed.py                 - Sample data loader
requirements.txt        - Python dependencies
