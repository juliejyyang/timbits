from sqlalchemy import create_engine, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# SQLalchemy MODELS --> maps python classes to database models, directly represents the database structure
class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    supabase_id = Column(String, unique=True, nullable=False)

    #relationships
    orders = relationship("PastOrders", back_populates="user", cascade="all, delete-orphan")

class PastOrders(Base):
    __tablename__ = "past_orders"
    id = Column(Integer, primary_key=True)

    #links this table to specific user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    total_calories = Column(Integer, default=0)
    
    #relationships
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("past_orders.id"), nullable=False)
    name = Column(String, nullable=False)
    calories = Column(Integer, default=0)
    quantity = Column(Integer, default=1)

    #relationships
    order = relationship("PastOrders", back_populates="items")


# Create the tables
Base.metadata.create_all(engine)

def seed():
    with SessionLocal() as session: 
        
        coffee = MenuItem(name="coffee", calories=70)
        tea = MenuItem(name="tea", calories=0)
        session.add_all([coffee, tea])

        test_user = User(email="test@example.com", supabase_id="test-1234567")
        session.add(test_user)
        session.commit()

def get_menu_db():
    menu_db = SessionLocal()
    try:
        yield menu_db
    finally:
        menu_db.close()

if __name__ == "__main__":
    seed()
