from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select

from .db import SessionLocal
from .models import Order, User

app = FastAPI(title="Shop")


class UserIn(BaseModel):
    name: str


@app.get("/users")
def list_users():
    with SessionLocal() as session:
        return [{"id": u.id, "name": u.name} for u in session.scalars(select(User).limit(50))]


@app.post("/users", status_code=201)
def create_user(body: UserIn):
    with SessionLocal.begin() as session:
        user = User(name=body.name)
        session.add(user)
        session.flush()
        return {"id": user.id, "name": user.name}


@app.get("/users/{user_id}/orders")
def list_orders(user_id: int):
    with SessionLocal() as session:
        orders = session.scalars(select(Order).where(Order.user_id == user_id))
        return [{"id": o.id, "total": str(o.total)} for o in orders]
