from fastapi import FastAPI, Query, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware # cross connection
from backend.menu_database import get_menu_db, MenuItem, PastOrders, OrderItem
from pydantic import BaseModel
from typing import List


app = FastAPI() 

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#Pydantic models for request/response validation
class OrderItemCreate(BaseModel):
    name: str
    calories: int
    quanitity: int = 1

class OrderCreate(BaseModel):
    items: List[dict]
    total_calories: int

class OrderResponse(BaseModel):
    id: int
    created_at: str
    total_calories: int

@app.get('/api/search')
async def search_items(item: str, db: Session = Depends(get_menu_db)):
    results = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{item}%")).all()
    return [{"id": r.id, "name": r.name, "calories": r.calories} for r in results]

@app.post('/api/orders')
async def create_order(order: OrderCreate, db: Session = Depends(get_menu_db)):
    past_order = PastOrders(total_calories=order.total_calories)
    
    for item in order.items:
        order_item = OrderItem(
            name=item['name'],
            calories=item['calories'],
            quantity=item.get('quantity', 1)
        )
        past_order.items.append(order_item)

    #save to database
    db.add(past_order)
    db.commit()
    db.refresh(past_order)

    return {"id": past_order.id, "created_at": past_order.created_at}

#get order history endpoint
@app.get('/api/orders')
async def get_order_history(db: Session = Depends(get_menu_db)):
    #retrieve all past orders with their items
    orders = db.query(PastOrders).order_by(PastOrders.created_at.desc()).all()

    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "created_at": order.created_at.isoformat(),
            "total_calories": order.total_calories,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "calories": item.calories,
                    "quanitity": item.quantity
                }
                for item in order.items
            ]
        })

    return result


