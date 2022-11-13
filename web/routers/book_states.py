from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_state_repo
from db.schemas import BookState, BookStateCreate


router = APIRouter()


@router.post("/", response_model=BookState, status_code=201)
def create(item: BookStateCreate, item_repo: Session = Depends(get_book_state_repo)):
    book_state = item_repo.create(item)
    
    return book_state


@router.get("/{item_id}", response_model=BookState, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_state_repo)):
    book_state = item_repo.read_by_id(item_id)
    
    if not book_state:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return book_state


@router.get("/", response_model=list[BookState | None], status_code=200)
def read(name: str | None = None, item_repo: Session = Depends(get_book_state_repo)):
    book_states = item_repo.read(name=name)
    
    return book_states


@router.put("/{item_id}", status_code=204)
def update(item: BookStateCreate, item_id: int, item_repo: Session = Depends(get_book_state_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_state_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")