"""Fill the database with production-sized data: 50,000 users and 200,000 orders.

An empty dev database hides almost every migration problem. This makes CI
behave like production does.
"""
from sqlalchemy import text

from app.db import engine

with engine.begin() as conn:
    conn.execute(text("INSERT INTO users (name) SELECT 'user ' || g FROM generate_series(1, 50000) g"))
    conn.execute(
        text(
            "INSERT INTO orders (user_id, total) "
            "SELECT 1 + (g % 50000), round((random() * 500)::numeric, 2) FROM generate_series(1, 200000) g"
        )
    )
print("Seeded 50,000 users and 200,000 orders.")
