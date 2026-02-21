from dotenv import load_dotenv
import os
from sqlmodel import SQLModel, Session, create_engine

load_dotenv()

# Heroku использует переменную окружения по умолчанию
DATABASE_URL = os.environ.get("DATABASE_URL")

# # Heroku требует замены схемы для SQLAlchemy
# if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
#     DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)