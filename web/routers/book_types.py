from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_type_repo
from db.schemas import BookType, BookTypeCreate


router = APIRouter()


@router.post("/", response_model=BookType, status_code=201)
def create(book_type: BookTypeCreate, book_type_repo: Session = Depends(get_book_type_repo)):
    db_book_type = book_type_repo.create(book_type)
    
    return db_book_type


@router.get("/{book_type_id}", response_model=BookType, status_code=200)
def read_by_id(book_type_id: int, book_type_repo: Session = Depends(get_book_type_repo)):
    db_book_type = book_type_repo.read_by_id(book_type_id)
    
    if not db_book_type:
        raise HTTPException(status_code=404, detail="Book Type not found")
    
    return db_book_type


@router.get("/", response_model=list[BookType | None], status_code=200)
def read(name: str | None = None, book_type_repo: Session = Depends(get_book_type_repo)):
    db_book_type_list = book_type_repo.read(name)
    
    return db_book_type_list


@router.put("/{book_type_id}", status_code=200)
def update(book_type: BookTypeCreate, book_type_id: int, book_type_repo: Session = Depends(get_book_type_repo)):
    book_type_repo.update(book_type=book_type, book_type_id=book_type_id)

    return {"status code": 200}


@router.delete("/{book_type_id}", status_code=200)
def delete(book_type_id: int, book_type_repo: Session = Depends(get_book_type_repo)):
    db_response = book_type_repo.delete(book_type_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Book Type not found")
    
    return {"status code": 200}