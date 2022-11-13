from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_decommision_repo
from db.schemas import BookDecommision, BookDecommisionCreate


router = APIRouter()


@router.post("/", response_model=BookDecommision, status_code=201)
def create(item: BookDecommisionCreate, item_repo: Session = Depends(get_book_decommision_repo)):
    book_decommision = item_repo.create(item)
    
    return book_decommision


@router.get("/{item_id}", response_model=BookDecommision, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_decommision_repo)):
    book_decommision = item_repo.read_by_id(item_id)
    
    if not book_decommision:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return book_decommision


@router.get("/", response_model=list[BookDecommision | None], status_code=200)
def read(books_total: int | None = None, item_repo: Session = Depends(get_book_decommision_repo)):
    book_decommisions = item_repo.read(books_total=books_total)
    
    return book_decommisions


@router.put("/{item_id}", status_code=204)
def update(item: BookDecommisionCreate, item_id: int, item_repo: Session = Depends(get_book_decommision_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_decommision_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")