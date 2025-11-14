from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = "postgresql+psycopg://banco_dizai_user:qhQ2gyuq9S1rVnwNcpCH6YgPawmB5nR7@dpg-d42osver433s73drgib0-a/banco_dizai"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
