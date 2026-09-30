# alembic-guard demo

A small FastAPI + Alembic shop app, used to show
[alembic-guard](https://github.com/ShalomHunukumbura/alembic-guard) catching a
dangerous migration in a pull request.

![alembic-guard on the two branches](docs/demo.gif)

## The two pull requests

Both PRs build the same feature: **add an email address to users, and link
orders to users with a foreign key.**

| PR | Migration | alembic-guard | Migration on production-sized data |
|----|-----------|---------------|------------------------------------|
| **Add user email** | The version most of us would write first | ❌ 2 errors, 2 warnings, annotated on the diff | ❌ Crashes: `NotNullViolation` |
| **Add user email (zero-downtime)** | Same feature, written safely | ✅ Clean | ✅ Passes |

The first migration looks fine in review and passes against an empty dev
database. It only breaks on a table that already has rows, which is exactly
where it runs in production.

## What CI does on every PR

`.github/workflows/migrations.yml` runs two jobs:

1. **alembic-guard** reads the migrations the PR adds and annotates risky lines
   directly on the diff. No database needed.
2. **Run migrations on production-sized data** migrates a fresh Postgres to the
   base branch, seeds it with 50,000 users and 200,000 orders, then applies the
   PR's migrations. This is the proof that the warnings are real.

In a real project you'd keep job 1. Job 2 is here to show the problems are real.

## Run it locally

```bash
docker compose up -d                    # Postgres on localhost:5434
uv sync
uv run alembic upgrade head
uv run python -m scripts.seed
uv run uvicorn app.main:app --reload    # http://localhost:8000/docs

uv run alembic-guard                    # lint every migration
```
