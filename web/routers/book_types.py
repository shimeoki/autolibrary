from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from web.dependencies import get_book_type_repo
from db.schemas import BookType, BookTypeCreate


router = APIRouter()


@router.post("/", response_model=BookType)
def create_book_type(book_type: BookTypeCreate, book_type_repo: Session = Depends(get_book_type_repo)):
    db_book_type = book_type_repo.create(book_type)
    
    return db_book_type


@router.get("/{book_type_id}", response_model=BookType)
def read_book_type(book_type_id: int, book_type_repo: Session = Depends(get_book_type_repo)):
    db_book_type = book_type_repo.read(book_type_id)
    # проверка на отсутствие
    return db_book_type