from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from web.dependencies import get_db
from db import crud, schemas


router = APIRouter()


@router.post("/", response_model=schemas.BookType)
def create_book_type(book_type: schemas.BookTypeCreate, session: Session = Depends(get_db)):
    methods = crud.BookTypeRepo(session=session)
    
    db_book_type = methods.create(book_type=book_type)
    
    return db_book_type