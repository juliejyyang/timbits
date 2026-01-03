import os
from fastapi import FastAPI, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware # cross connection
from backend.menu_database import get_menu_db, MenuItem, PastOrders, OrderItem, User
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List
import jwt


app = FastAPI() 
security = HTTPBearer()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://timbits.vercel.app/"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

#initialize supabase client base
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

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

# PYDANTIC MODELS for request bodies --> used for data validation (in this case validates incoming api requests), parsing, and serialization using Python type hints
class UserCredentials(BaseModel):
    email: str
    password: str
class UserResponse(BaseModel):
    email: str
    id: str

#Function to get current user from token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_menu_db)
):
    token = credentials.credentials

    try:
        user_response = supabase.auth.get_user(token)
        supabase_user = user_response.user

        if not supabase_user:
            raise HTTPException(status_code=401, detail="Invalid token")

        #get or create user in your database
        db_user = db.query(User).filter(User.supabase_id == supabase_user.id).first()
        if not db_user:
            db_user = User(
                email=supabase_user.email,
                supabase_id=supabase_user.id
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        
        return db_user
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid authentication: {str(e)}")


@app.post("/signup", response_model=UserResponse)
async def user_signup(credentials: UserCredentials):
    try:
        #sign up the user with email and password
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })

        user = res.user

        if user:
            return UserResponse(email=user.email, id=user.id)
        else:
            raise HTTPException (
                status_code=status.HTTP_200_OK,
                detail="Sign up successful. Please check your email for verification link"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {e.args[0]}"
        )

@app.post("/login")
async def user_login(credentials: UserCredentials):
    try:
        #sign in user with email and password
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email, 
            "password": credentials.password
        })
        return {"message": "Login success", "access_token": res.session.access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {e.args[0]}"
        )


@app.get('/api/search')
async def search_items(item: str, db: Session = Depends(get_menu_db)):
    results = db.query(MenuItem).filter(MenuItem.name.ilike(f"%{item}%")).all()
    return [{"id": r.id, "name": r.name, "calories": r.calories} for r in results]

#save orders with usre authentication
@app.post('/api/orders')
async def create_order(
    order: OrderCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_menu_db)
):
    
    new_order = PastOrders(
        user_id=current_user.id,
        total_calories=order.total_calories
    )
     #save to database
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # add order items
    for item in order.items:
        order_item = OrderItem(
            order_id=new_order.id,
            name=item['name'],
            calories=item['calories'],
            quantity=item.get('quantity', 1)
        )
        db.add(order_item)
    
    db.commit()
   
    return {"message": "Order saved", "order_id": new_order.id}

#get order history endpoint, only for authenticated user
@app.get('/api/orders')
async def get_order_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_menu_db)
):
    #retrieve all past orders with their items, for the current user
    orders = db.query(PastOrders).filter(
        PastOrders.user_id == current_user.id
    ).order_by(PastOrders.created_at.desc()).all()

    return [
        {
            "id": order.id,
            "created_at": order.created_at.isoformat(),
            "total_calories": order.total_calories,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "calories": item.calories,
                    "quantity": item.quantity
                }
                for item in order.items
            ]
        }
        for order in orders
    ]




