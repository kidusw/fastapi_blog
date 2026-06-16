# FastAPI Blog

A full-featured blog platform built with FastAPI, featuring a REST API alongside server-rendered HTML pages. Users can register, create posts, manage their profile, and recover their password via email.

## Features

- JWT authentication with Argon2 password hashing
- Create, read, update, and delete blog posts
- User profile management with profile picture uploads
- Password reset via email (HTML email template)
- Paginated post listings
- Dual interface: JSON REST API (`/api/`) and server-rendered HTML pages
- PostgreSQL with async SQLAlchemy 2.0 and Alembic migrations

## Tech Stack

| Layer | Library |
|---|---|
| Web framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Auth | PyJWT + pwdlib (Argon2) |
| Templates | Jinja2 |
| Email | aiosmtplib |
| Images | Pillow |
| Config | pydantic-settings |

Requires **Python 3.13+**.

## Project Structure

```
fastapi_blog/
├── main.py              # App entry point, HTML routes, exception handlers
├── models.py            # SQLAlchemy ORM models (User, Post, PasswordResetToken)
├── schemas.py           # Pydantic request/response schemas
├── database.py          # Async DB engine and session dependency
├── config.py            # Settings loaded from .env
├── auth.py              # JWT creation/verification, password hashing, dependencies
├── email_utils.py       # Async email sending
├── image_utils.py       # Profile picture resizing and storage
├── populate_db.py       # Script to seed the database with test data
├── routers/
│   ├── users.py         # /api/users endpoints
│   └── posts.py         # /api/posts endpoints
├── templates/           # Jinja2 HTML templates
├── static/              # CSS, JS, and static assets
├── media/               # User-uploaded profile pictures
└── alembic/             # Database migration scripts
```

## Getting Started

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd fastapi_blog
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Configure environment

Copy the example below into a `.env` file at the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fastapi_blog

# Email (Mailtrap sandbox works for development)
MAIL_SERVER=sandbox.smtp.mailtrap.io
MAIL_PORT=2525
MAIL_USERNAME=your-mailtrap-username
MAIL_PASSWORD=your-mailtrap-password
MAIL_FROM=noreply@example.com

FRONTEND_URL=http://localhost:8000
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start the server

```bash
fastapi dev main.py
```

The app will be available at `http://localhost:8000`.

### 5. (Optional) Seed the database

```bash
python populate_db.py
```

This creates 6 test users and 44 sample posts so you have data to work with immediately.

## API Reference

All API endpoints are prefixed with `/api`.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/users/` | Register a new user |
| `POST` | `/api/users/token` | Login — returns a JWT access token |
| `GET` | `/api/users/me` | Get current user (requires auth) |

### Users

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/users/{user_id}` | Get public user profile |
| `GET` | `/api/users/{user_id}/posts` | Get paginated posts for a user |
| `PATCH` | `/api/users/{user_id}` | Update username or email (requires auth) |
| `DELETE` | `/api/users/{user_id}` | Delete account (requires auth) |
| `PATCH` | `/api/users/{user_id}/picture` | Upload profile picture (requires auth) |
| `DELETE` | `/api/users/{user_id}/picture` | Remove profile picture (requires auth) |
| `PATCH` | `/api/users/me/password` | Change password (requires auth) |
| `POST` | `/api/users/forgot-password` | Request a password reset email |
| `POST` | `/api/users/reset-password` | Reset password with emailed token |

### Posts

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/posts/` | List all posts (paginated) |
| `POST` | `/api/posts/` | Create a post (requires auth) |
| `GET` | `/api/posts/{post_id}` | Get a single post |
| `PUT` | `/api/posts/{post_id}` | Full update (requires auth) |
| `PATCH` | `/api/posts/{post_id}` | Partial update (requires auth) |
| `DELETE` | `/api/posts/{post_id}` | Delete a post (requires auth) |

Pagination uses `skip` and `limit` query parameters. Responses include `total`, `has_more`, `skip`, and `limit` fields.

### Authentication header

Protected endpoints require a Bearer token:

```
Authorization: Bearer <access_token>
```

## Configuration Reference

All settings are loaded from `.env` via pydantic-settings.

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | — | JWT signing key (required) |
| `DATABASE_URL` | — | SQLAlchemy async database URL (required) |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT token lifetime |
| `RESET_TOKEN_EXPIRE_MINUTES` | `60` | Password reset token lifetime |
| `POSTS_PER_PAGE` | `10` | Default pagination page size |
| `MAX_UPLOAD_SIZE_BYTES` | `5242880` | Profile picture upload limit (5 MB) |
| `MAIL_SERVER` | — | SMTP server host |
| `MAIL_PORT` | — | SMTP server port |
| `MAIL_USERNAME` | — | SMTP username |
| `MAIL_PASSWORD` | — | SMTP password |
| `MAIL_FROM` | — | Sender address for outgoing emails |
| `FRONTEND_URL` | — | Base URL included in password reset links |

## Database Migrations

Migrations are managed with Alembic.

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after changing models.py
alembic revision --autogenerate -m "describe your change"

# Roll back one migration
alembic downgrade -1
```
