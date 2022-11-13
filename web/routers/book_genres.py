from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_genre_repo
from db.schemas import BookGenre, BookGenreCreate


router = APIRouter()


@router.post("/", response_model=BookGenre, status_code=201)
def create(item: BookGenreCreate, item_repo: Session = Depends(get_book_genre_repo)):
    book_genre = item_repo.create(item)
    
    return book_genre


@router.get("/{item_id}", response_model=BookGenre, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_genre_repo)):
    book_genre = item_repo.read_by_id(item_id)
    
    if not book_genre:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return book_genre


@router.get("/", response_model=list[BookGenre | None], status_code=200)
def read(name: str | None = None, item_repo: Session = Depends(get_book_genre_repo)):
    book_genres = item_repo.read(name=name)
    
    return book_genres


@router.put("/{item_id}", status_code=204)
def update(item: BookGenreCreate, item_id: int, item_repo: Session = Depends(get_book_genre_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_genre_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")