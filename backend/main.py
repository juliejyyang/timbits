from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware # cross connection
from backend.menu_database import get_menu_db, MenuItem


app = FastAPI() 

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get('/api/search')
async def search_items(item: str, db: Session = Depends(get_menu_db)):
    results = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{item}%")).all()
    return [{"id": r.id, "name": r.name, "calories": r.calories} for r in results]


