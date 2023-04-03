from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_book_repo
from db.schemas import Book, BookCreate, BookToGive


router = APIRouter()


@router.post("/", response_model=Book, status_code=201)
def create(item: BookCreate, item_repo: Session = Depends(get_book_repo)):
    book = item_repo.create(item)
    
    return book


@router.get("/pending", response_model=list[Book | None], status_code=200)
def read_pending(item_repo: Session = Depends(get_book_repo)):
    books = item_repo.read_pending()
    
    return books


@router.get("/available", response_model=list[Book | None], status_code=200)
def search_available(title: str | None = None, author: str | None = None, item_repo: Session = Depends(get_book_repo)):
    books = item_repo.search_available(title=title, author=author)
    
    return books


@router.get("/{item_id}", response_model=Book, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_book_repo)):
    book = item_repo.read_by_id(item_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@router.get("/", response_model=list[Book | None], status_code=200)
def read(title: str | None = None, author: str | None = None, student_id: int | None = None, item_repo: Session = Depends(get_book_repo)):
    books = item_repo.read(title=title, author=author, student_id=student_id)
    
    return books


@router.put("/on_hands_book/{item_id}", status_code=204)
def on_hands_book(item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.on_hands_book(item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Something not found")@router.put("/queue_book/{item_id}", status_code=204)


@router.put("/to_give_book/{item_id}", status_code=204)
def to_give_book(item: BookToGive, item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.to_give_book(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Something not found")


@router.put("/queue_book/{item_id}", status_code=204)
def queue_book(student_id: int, item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.queue_book(student_id=student_id, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Something not found")


@router.put("/clear_book/{item_id}", status_code=204)
def clear_book(item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.clear_book(item_id=item_id)
    
    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Something not found")


@router.put("/{item_id}", status_code=204)
def update(item: BookCreate, item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Something not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_book_repo)):
    response = item_repo.delete(item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")