from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_repo
from db.schemas import Book, BookCreate, BookPatch


router = APIRouter()


@router.post("/", response_model=Book, status_code=201)
def create(book: BookCreate, book_repo: Session = Depends(get_book_repo)):
    db_book = book_repo.create(book)
    
    return db_book


@router.get("/pending", response_model=list[Book | None], status_code=200)
def read_pending(book_repo: Session = Depends(get_book_repo)):
    db_book_list = book_repo.read_pending()
    
    return db_book_list


@router.get("/{book_id}", response_model=Book, status_code=200)
def read_by_id(book_id: int, book_repo: Session = Depends(get_book_repo)):
    db_book = book_repo.read_by_id(book_id)
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return db_book


@router.get("/", response_model=list[Book | None], status_code=200)
def read(book_repo: Session = Depends(get_book_repo)):
    db_book_list = book_repo.read()
    
    return db_book_list


@router.put("/{book_id}", status_code=200)
def update(book: BookCreate, book_id: int, book_repo: Session = Depends(get_book_repo)):
    book_repo.update(book=book, book_id=book_id)

    return {"status code": 200}


@router.patch("/{book_id}", status_code=200)
def patch(book: BookPatch, book_id: int, book_repo: Session = Depends(get_book_repo)):
    book_repo.patch(book=book, book_id=book_id)
    
    return {"status code": 200}


@router.delete("/{book_id}", status_code=200)
def delete(book_id: int, book_repo: Session = Depends(get_book_repo)):
    db_response = book_repo.delete(book_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"status code": 200}