import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg://shop:shop@localhost:5434/shop")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine)
