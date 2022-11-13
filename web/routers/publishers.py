from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_publisher_repo
from db.schemas import Publisher, PublisherCreate


router = APIRouter()


@router.post("/", response_model=Publisher, status_code=201)
def create(item: PublisherCreate, item_repo: Session = Depends(get_publisher_repo)):
    publisher = item_repo.create(item)
    
    return publisher


@router.get("/{item_id}", response_model=Publisher, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_publisher_repo)):
    publisher = item_repo.read_by_id(item_id)
    
    if not publisher:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return publisher


@router.get("/", response_model=list[Publisher | None], status_code=200)
def read(name: str | None = None, city: str | None = None, item_repo: Session = Depends(get_publisher_repo)):
    publishers = item_repo.read(name=name, city=city)
    
    return publishers


@router.put("/{item_id}", status_code=204)
def update(item: PublisherCreate, item_id: int, item_repo: Session = Depends(get_publisher_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_publisher_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")