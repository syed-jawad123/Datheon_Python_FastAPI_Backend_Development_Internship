"""
Datheon Python + FastAPI Backend Development Internship
Task 2: User Authentication & RBAC with JWT
Application ID: DT-2026-89H4F | Candidate: Syed Jawad Hussain Shah
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "datheon-super-secure-production-jwt-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(
    title="Datheon JWT Authentication & RBAC API",
    description="FastAPI service with Bcrypt hashing, signed JWT tokens, and Role-Based Access Control.",
    version="1.0.0"
)

class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: RoleEnum = Field(default=RoleEnum.USER)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleEnum
    expires_in_seconds: int

users_db = {}
user_seq = 0

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

async def require_admin_role(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admin privileges required."
        )
    return current_user

@app.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user_in: UserRegister):
    global user_seq
    if user_in.username in users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    user_seq += 1
    new_user = {
        "id": user_seq,
        "username": user_in.username,
        "email": user_in.email,
        "hashed_password": hash_password(user_in.password),
        "role": user_in.role,
        "is_active": True
    }
    users_db[user_in.username] = new_user
    return new_user

@app.post("/auth/login", response_model=TokenResponse, status_code=status.HTTP_200_OK, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
        "expires_in_seconds": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@app.get("/users/me", response_model=UserOut, tags=["Users"])
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.get("/admin/dashboard", tags=["Admin"])
def get_admin_dashboard(admin_user: dict = Depends(require_admin_role)):
    return {
        "message": f"Welcome Administrator {admin_user['username']}! Full system access granted.",
        "total_users": len(users_db),
        "system_status": "All security layers nominal."
    }
