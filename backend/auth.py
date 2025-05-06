from fastapi import APIRouter, HTTPException, Depends
from database import SessionLocal
from images import get_current_user
from controllers.user_controller import register_user, login_user, get_profile, update_profile, change_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
async def register(data: dict, db=Depends(get_db)):
    return await register_user(data, db)

@router.post("/login")
async def login(data: dict, db=Depends(get_db)):
    return await login_user(data, db)

@router.get("/me")
async def get_me(user=Depends(get_current_user)):
    return await get_profile(user)

@router.put("/profile")
async def update_profile_route(data: dict, user=Depends(get_current_user), db=Depends(get_db)):
    return await update_profile(data, user, db)

@router.put("/password")
async def change_password_route(data: dict, user=Depends(get_current_user), db=Depends(get_db)):
    return await change_password(data, user, db) 