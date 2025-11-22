from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session 

DATABASE_URL = "postgresql://postgres:Trevvy781@localhost/tims"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_menu_db():
    menu_db = SessionLocal()
    try:
        yield menu_db
    finally:
        menu_db.close()

