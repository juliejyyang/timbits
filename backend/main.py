from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from menu_database import get_menu_db
from models import MenuItem

app = FastAPI() 

@app.get('/api/search')
async def search_items(item: str, db: Session = Depends(get_menu_db)):
    result = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{item}%"))
    return [selected_item.calories for selected_item in result]


