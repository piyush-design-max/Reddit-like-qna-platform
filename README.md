# QandAPlatform

A Reddit-style Q&A platform built with FastAPI, PostgreSQL, and JWT authentication — with an AI-powered answer summarization feature using Groq's LLM API. Deployed live on Railway.

## Features

- User registration and login with JWT authentication
- Post questions and answers
- Search questions by keyword
- Upvote/downvote system with composite key constraints to prevent duplicate votes
- **AI-generated answer summaries** — automatically synthesizes all answers to a question into a concise overview using Groq's Llama model, regenerated whenever a new answer is posted (not on every read, for efficiency)
- Ownership enforcement — users can only delete their own questions and answers
- Relational data model with proper foreign keys and cascading deletes
- Environment-based configuration for secrets and database credentials

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM combining SQLAlchemy and Pydantic
- **PostgreSQL** — database
- **JWT (PyJWT)** — authentication
- **Groq API** — LLM-powered answer summarization
- **pwdlib** — password hashing
- **Pydantic Settings** — environment variable management
- **Railway** — deployment (app + managed PostgreSQL)

## Project Structure

```
app/
├── main.py           # FastAPI app and router registration
├── models.py         # SQLModel database models (User, Questions, Answers, Votes)
├── schemas.py        # Pydantic schemas for requests/responses
├── database.py       # Database connection and session dependency
├── config.py         # Environment variable configuration
├── oauth2.py         # JWT token creation and verification
├── utils.py          # Password hashing utilities
├── ai.py             # Groq LLM integration for answer summarization
└── routers/
    ├── auth.py           # Login route
    ├── questions.py       # Question CRUD, search, answers, voting, delete
    └── vote.py            # Voting logic
```

## Database Schema

- **users** — user_id, username, password (hashed), created_at
- **questions** — question_id, title, content, user_id (FK), vote count, ai_overview, created_at
- **answers** — answer_id, content, user_id (FK), question_id (FK), created_at
- **votes** — composite primary key (question_id, user_id) with CASCADE delete

## API Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |

### Questions
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | `/questions/` | Ask a question | Yes |
| GET | `/questions/` | List all questions | No |
| GET | `/questions/search?q=` | Search questions by keyword | No |
| GET | `/questions/{id}` | Get question with answers + AI summary | No |
| POST | `/questions/{id}/answer` | Post an answer (triggers AI re-summarization) | Yes |
| DELETE | `/questions/delete` | Delete your own question or answer | Yes |

### Votes
| Method | Route | Description | Auth Required |
|--------|-------|-------------|---------------|
| POST | `/vote` | Upvote or downvote a question | Yes |

## Setup (Local)

**1. Clone the repo**
```bash
git clone https://github.com/piyush-design-max/Reddit-like-qna-platform.git
cd Reddit-like-qna-platform
```

**2. Create and activate virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file**
```
database_hostname=localhost
database_port=5432
database_password=yourpassword
database_name=qandaplatform
database_username=postgres
secret_key=your_secret_key
algorithm=HS256
access_token_expire_minutes=30
groq_api_key=your_groq_api_key
```

**5. Create a PostgreSQL database matching your `.env` config**

**6. Run the server**
```bash
uvicorn app.main:app --reload
```

**7. Open API docs**
```
http://127.0.0.1:8000/docs
```

## Deployment

Deployed on **Railway** with a separate managed PostgreSQL instance in the same project. The web service reads database credentials and secrets from Railway's environment variables (no `.env` file in production — `pydantic-settings` reads directly from the OS environment, same mechanism as a local `.env` file).

Start command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Why AI Summaries Are Cached, Not Generated on Read

Rather than calling the LLM every time a question is viewed, the summary is generated once when a new answer is posted and stored directly in the `ai_overview` column. This avoids redundant API calls, reduces latency for readers, and keeps token usage predictable.

## Authentication

Protected routes require a Bearer token obtained from `/login`:

```
Authorization: Bearer <your_token>
```
