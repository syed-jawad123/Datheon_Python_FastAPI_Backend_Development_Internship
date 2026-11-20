"""
Datheon Python + FastAPI Backend Development Internship
Task 1: BookStore REST API with Pydantic Validation
Application ID: DT-2026-89H4F | Candidate: Syed Jawad Hussain Shah
"""

from typing import List, Optional
from enum import Enum
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(
    title="Datheon BookStore REST API",
    description="Asynchronous CRUD REST API with Pydantic Validation, filtering, and OpenAPI documentation.",
    version="1.0.0"
)

class GenreEnum(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    TECH = "Technology"
    SCIENCE = "Science"
    PHILOSOPHY = "Philosophy"

class BookBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Title of the book")
    author: str = Field(..., min_length=2, max_length=100, description="Author full name")
    genre: GenreEnum = Field(..., description="Genre category")
    price: float = Field(..., gt=0, description="Retail price in USD")
    published_year: int = Field(..., ge=1800, le=2030, description="Year of publication")
    stock: int = Field(default=0, ge=0, description="Available inventory stock")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=150)
    author: Optional[str] = Field(None, min_length=2, max_length=100)
    genre: Optional[GenreEnum] = None
    price: Optional[float] = Field(None, gt=0)
    published_year: Optional[int] = Field(None, ge=1800, le=2030)
    stock: Optional[int] = Field(None, ge=0)

class BookResponse(BookBase):
    id: int = Field(..., description="Unique auto-assigned book ID")
    model_config = ConfigDict(from_attributes=True)

# In-memory storage mock database
db_books = {
    1: {"id": 1, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "genre": GenreEnum.TECH, "price": 44.99, "published_year": 2017, "stock": 25},
    2: {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "genre": GenreEnum.TECH, "price": 38.50, "published_year": 2008, "stock": 18},
    3: {"id": 3, "title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari", "genre": GenreEnum.NON_FICTION, "price": 22.00, "published_year": 2014, "stock": 40},
    4: {"id": 4, "title": "Atomic Habits", "author": "James Clear", "genre": GenreEnum.PHILOSOPHY, "price": 19.99, "published_year": 2018, "stock": 50}
}
book_id_seq = 4

@app.get("/", tags=["Root"])
def root():
    return {
        "status": "online",
        "program": "Datheon Python + FastAPI Backend Internship",
        "app_id": "DT-2026-89H4F",
        "docs_url": "/docs"
    }

@app.get("/books", response_model=List[BookResponse], status_code=status.HTTP_200_OK, tags=["Books"])
def get_books(
    genre: Optional[GenreEnum] = Query(None, description="Filter by genre"),
    author: Optional[str] = Query(None, description="Partial or full match on author name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    skip: int = Query(0, ge=0, description="Pagination skip offset"),
    limit: int = Query(10, ge=1, le=100, description="Pagination max items per page")
):
    results = list(db_books.values())
    if genre:
        results = [b for b in results if b["genre"] == genre]
    if author:
        results = [b for b in results if author.lower() in b["author"].lower()]
    if min_price is not None:
        results = [b for b in results if b["price"] >= min_price]
    if max_price is not None:
        results = [b for b in results if b["price"] <= max_price]
    return results[skip : skip + limit]

@app.get("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK, tags=["Books"])
def get_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    return db_books[book_id]

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, tags=["Books"])
def create_book(book_in: BookCreate):
    global book_id_seq
    book_id_seq += 1
    new_book = book_in.model_dump()
    new_book["id"] = book_id_seq
    db_books[book_id_seq] = new_book
    return new_book

@app.put("/books/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK, tags=["Books"])
def update_book(book_id: int, book_update: BookUpdate):
    if book_id not in db_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    current_book = db_books[book_id]
    update_data = book_update.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        current_book[field] = val
    db_books[book_id] = current_book
    return current_book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Books"])
def delete_book(book_id: int):
    if book_id not in db_books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id} not found")
    del db_books[book_id]
    return None
