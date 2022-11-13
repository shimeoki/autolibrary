from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_student_repo
from db.schemas import Student, StudentCreate


router = APIRouter()


@router.post("/", response_model=Student, status_code=201)
def create(item: StudentCreate, item_repo: Session = Depends(get_student_repo)):
    student = item_repo.create(item)
    
    return student


@router.get("/{item_id}", response_model=Student, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_student_repo)):
    student = item_repo.read_by_id(item_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return student


@router.get("/", response_model=list[Student | None], status_code=200)
def read(
    first_name: str | None = None, 
    last_name: str | None = None,
    login: str | None = None, 
    item_repo: Session = Depends(get_student_repo)
):
    students = item_repo.read(first_name=first_name, last_name=last_name, login=login)
    
    return students


@router.put("/{item_id}", status_code=204)
def update(item: StudentCreate, item_id: int, item_repo: Session = Depends(get_student_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_student_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")