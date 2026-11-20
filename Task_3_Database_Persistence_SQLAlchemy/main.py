"""
Datheon Python + FastAPI Backend Development Internship
Task 3: Database Persistence with SQLAlchemy & SQLite
Application ID: DT-2026-89H4F | Candidate: Syed Jawad Hussain Shah
"""

from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Datheon SQLAlchemy Relational Persistence API",
    description="Relational database persistence layer with User -> Notes relationships and Foreign Key joins.",
    version="1.0.0"
)

@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=List[schemas.UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserDetailResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/notes", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED, tags=["Notes"])
def create_note_for_user(user_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_note(db=db, note=note, user_id=user_id)

@app.get("/notes", response_model=List[schemas.NoteResponse], tags=["Notes"])
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_notes(db, skip=skip, limit=limit)
