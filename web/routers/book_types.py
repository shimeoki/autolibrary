from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_type_repo
from db.schemas import BookType, BookTypeCreate


router = APIRouter()


@router.post("/", response_model=BookType, status_code=201)
def create(item: BookTypeCreate, item_repo: Session = Depends(get_book_type_repo)):
    book_type = item_repo.create(item)
    
    return book_type


@router.get("/{item_id}", response_model=BookType, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_type_repo)):
    book_type = item_repo.read_by_id(item_id)
    
    if not book_type:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return book_type


@router.get("/", response_model=list[BookType | None], status_code=200)
def read(name: str | None = None, item_repo: Session = Depends(get_book_type_repo)):
    book_types = item_repo.read(name=name)
    
    return book_types


@router.put("/{item_id}", status_code=204)
def update(item: BookTypeCreate, item_id: int, item_repo: Session = Depends(get_book_type_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_type_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")