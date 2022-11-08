from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_publisher_repo
from db.schemas import Publisher, PublisherCreate


router = APIRouter()


@router.post("/", response_model=Publisher, status_code=201)
def create(publisher: PublisherCreate, publisher_repo: Session = Depends(get_publisher_repo)):
    db_publisher = publisher_repo.create(publisher)
    
    return db_publisher


@router.get("/{publisher_id}", response_model=Publisher, status_code=200)
def read_by_id(publisher_id: int, publisher_repo: Session = Depends(get_publisher_repo)):
    db_publisher = publisher_repo.read_by_id(publisher_id)
    
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    
    return db_publisher


@router.get("/", response_model=list[Publisher | None], status_code=200)
def read(name: str | None = None, city: str | None = None, publisher_repo: Session = Depends(get_publisher_repo)):
    db_publisher_list = publisher_repo.read(name=name, city=city)
    
    return db_publisher_list


@router.put("/{publisher_id}", status_code=200)
def update(publisher: PublisherCreate, publisher_id: int, publisher_repo: Session = Depends(get_publisher_repo)):
    publisher_repo.update(publisher=publisher, publisher_id=publisher_id)

    return {"status code": 200}


@router.delete("/{publisher_id}", status_code=200)
def delete(publisher_id: int, publisher_repo: Session = Depends(get_publisher_repo)):
    db_response = publisher_repo.delete(publisher_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Publisher not found")
    
    return {"status code": 200}