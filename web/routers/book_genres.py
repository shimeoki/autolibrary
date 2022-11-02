from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_genre_repo
from db.schemas import BookGenre, BookGenreCreate


router = APIRouter()


@router.post("/", response_model=BookGenre, status_code=201)
def create(book_genre: BookGenreCreate, book_genre_repo: Session = Depends(get_book_genre_repo)):
    db_book_genre = book_genre_repo.create(book_genre)
    
    return db_book_genre


@router.get("/{book_genre_id}", response_model=BookGenre, status_code=200)
def read(book_genre_id: int, book_genre_repo: Session = Depends(get_book_genre_repo)):
    db_book_genre = book_genre_repo.read(book_genre_id)
    
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="Book Genre not found")
    
    return db_book_genre


@router.get("/", response_model=list[BookGenre | None], status_code=200)
def read_all(book_genre_repo: Session = Depends(get_book_genre_repo)):
    db_book_genre_list = book_genre_repo.read_all()
    
    return db_book_genre_list


@router.put("/{book_genre_id}", status_code=200)
def update(book_genre: BookGenreCreate, book_genre_id: int, book_genre_repo: Session = Depends(get_book_genre_repo)):
    book_genre_repo.update(book_genre=book_genre, book_genre_id=book_genre_id)

    return {"status code": 200}


@router.delete("/{book_genre_id}", status_code=200)
def delete(book_genre_id: int, book_genre_repo: Session = Depends(get_book_genre_repo)):
    db_response = book_genre_repo.delete(book_genre_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Book Genre not found")
    
    return {"status code": 200}