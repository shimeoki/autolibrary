from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_state_repo
from db.schemas import BookState, BookStateCreate


router = APIRouter()


@router.post("/", response_model=BookState, status_code=201)
def create(book_state: BookStateCreate, book_state_repo: Session = Depends(get_book_state_repo)):
    db_book_state = book_state_repo.create(book_state)
    
    return db_book_state


@router.get("/{book_state_id}", response_model=BookState, status_code=200)
def read_by_id(book_state_id: int, book_state_repo: Session = Depends(get_book_state_repo)):
    db_book_state = book_state_repo.read_by_id(book_state_id)
    
    if not db_book_state:
        raise HTTPException(status_code=404, detail="Book State not found")
    
    return db_book_state


@router.get("/", response_model=list[BookState | None], status_code=200)
def read(name: str | None = None, book_state_repo: Session = Depends(get_book_state_repo)):
    db_book_state_list = book_state_repo.read(name)
    
    return db_book_state_list


@router.put("/{book_state_id}", status_code=200)
def update(book_state: BookStateCreate, book_state_id: int, book_state_repo: Session = Depends(get_book_state_repo)):
    book_state_repo.update(book_state=book_state, book_state_id=book_state_id)

    return {"status code": 200}


@router.delete("/{book_state_id}", status_code=200)
def delete(book_state_id: int, book_state_repo: Session = Depends(get_book_state_repo)):
    db_response = book_state_repo.delete(book_state_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Book State not found")
    
    return {"status code": 200}