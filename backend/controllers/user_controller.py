from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt
from fastapi import HTTPException
from models import User
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET")

async def register_user(data, db):
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")
    if not all([first_name, last_name, email, password, phone]):
        raise HTTPException(status_code=400, detail="All fields required")
    hashed = pwd_context.hash(password)
    user = User(first_name=first_name, last_name=last_name, email=email, password_hash=hashed, phone=phone)
    db.add(user)
    try:
        await db.commit()
        return {"first_name": first_name, "last_name": last_name, "email": email, "phone": phone}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

async def login_user(data, db):
    email = data.get("email")
    password = data.get("password")
    if not all([email, password]):
        raise HTTPException(status_code=400, detail="All fields required")
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"id": user.id, "email": user.email}, JWT_SECRET, algorithm="HS256")
    return {"token": token, "first_name": user.first_name, "last_name": user.last_name}

async def get_profile(user):
    return {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "phone": user.phone}

async def update_profile(data, user, db):
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    phone = data.get("phone")
    if not all([first_name, last_name, email]):
        raise HTTPException(status_code=400, detail="First name, last name, and email are required")
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.phone = phone
    try:
        await db.commit()
        return {"success": True, "first_name": first_name, "last_name": last_name, "email": email, "phone": phone}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

async def change_password(data, user, db):
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not all([old_password, new_password]):
        raise HTTPException(status_code=400, detail="Old and new password required")
    if not pwd_context.verify(old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    user.password_hash = pwd_context.hash(new_password)
    await db.commit()
    return {"success": True} 