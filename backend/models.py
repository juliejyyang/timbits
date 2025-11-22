from sqlalchemy import Column, Integer, String
from menu_database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    calories = Column(Integer)