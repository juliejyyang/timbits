from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session 
from sqlalchemy import Column, Integer, String


DATABASE_URL = "postgresql://postgres:Trevvy781@localhost/tims"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# MODELS
class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)

# Create the tables
Base.metadata.create_all(engine)

def seed():
    with SessionLocal() as session: 
        coffee = MenuItem(name="coffee", calories=70)
        tea = MenuItem(name="tea", calories=0)
        session.add_all([coffee, tea])
        session.commit()

def get_menu_db():
    menu_db = SessionLocal()
    try:
        yield menu_db
    finally:
        menu_db.close()

if __name__ == "__main__":
    seed()
