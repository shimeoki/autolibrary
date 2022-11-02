from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_decommision_repo
from db.schemas import BookDecommision, BookDecommisionCreate


router = APIRouter()


@router.post("/", response_model=BookDecommision, status_code=201)
def create(book_decommision: BookDecommisionCreate, book_decommision_repo: Session = Depends(get_book_decommision_repo)):
    db_book_decommision = book_decommision_repo.create(book_decommision)
    
    return db_book_decommision


@router.get("/{book_decommision_id}", response_model=BookDecommision, status_code=200)
def read(book_decommision_id: int, book_decommision_repo: Session = Depends(get_book_decommision_repo)):
    db_book_decommision = book_decommision_repo.read(book_decommision_id)
    
    if not db_book_decommision:
        raise HTTPException(status_code=404, detail="Book Decommision not found")
    
    return db_book_decommision


@router.get("/", response_model=list[BookDecommision | None], status_code=200)
def read_all(book_decommision_repo: Session = Depends(get_book_decommision_repo)):
    db_book_decommision_list = book_decommision_repo.read_all()
    
    return db_book_decommision_list


@router.put("/{book_decommision_id}", status_code=200)
def update(book_decommision: BookDecommisionCreate, book_decommision_id: int, book_decommision_repo: Session = Depends(get_book_decommision_repo)):
    book_decommision_repo.update(book_decommision=book_decommision, book_decommision_id=book_decommision_id)

    return {"status code": 200}


@router.delete("/{book_decommision_id}", status_code=200)
def delete(book_decommision_id: int, book_decommision_repo: Session = Depends(get_book_decommision_repo)):
    db_response = book_decommision_repo.delete(book_decommision_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Book Decommision not found")
    
    return {"status code": 200}