# Mess Meal Expense Manager — Backend (Phase 1)

Phase 1 scope: Users + Meals CRUD, running on FastAPI + SQLAlchemy + SQLite.

## Run it

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs — Swagger UI where you can try every endpoint.

## Endpoints in this phase

| Method | Path                          | Purpose                          |
|--------|-------------------------------|-----------------------------------|
| POST   | /users                        | Create a user                     |
| GET    | /users                        | List all users                    |
| POST   | /meals                        | Log a meal entry for a user       |
| GET    | /meals?user_id=&month=YYYY-MM | List meals, optionally filtered   |
| GET    | /health                       | Health check                      |

## Try it (example flow)

1. `POST /users` with `{"name": "Rafi", "email": "rafi@example.com"}`
2. Copy the returned `id`.
3. `POST /meals` with `{"user_id": 1, "date": "2026-08-28", "lunch": ...}` —
   actually the body is `{"user_id": 1, "date": "2026-08-28", "meal_count": 2}`
4. `GET /meals?user_id=1&month=2026-08` to see it filtered.

## Rules enforced right now

- `meal_count` must be 0–3 (Pydantic `Field(ge=0, le=3)`).
- One meal entry per user per date (DB-level `UniqueConstraint`, returns 400 on violation).
- `email` must be unique across users.

## Checkpoint before moving to Phase 2

- [ ] Server starts with `uvicorn app.main:app --reload`
- [ ] You can create a user via `/docs`
- [ ] You can log a meal for that user
- [ ] Logging a duplicate date for the same user returns a 400, not a crash
- [ ] `GET /meals?user_id=1&month=2026-08` returns only that user's August entries

Once all boxes are checked, we move to **Phase 2: Expenses, Deposits & the Settlement Math** — the core "who owes whom" logic.
