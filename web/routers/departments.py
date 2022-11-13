from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_department_repo
from db.schemas import Department, DepartmentCreate


router = APIRouter()


@router.post("/", response_model=Department, status_code=201)
def create(item: DepartmentCreate, item_repo: Session = Depends(get_department_repo)):
    department = item_repo.create(item)
    
    return department


@router.get("/{item_id}", response_model=Department, status_code=200)
def read_by_id(item_id: int, item_repo: Session = Depends(get_department_repo)):
    department = item_repo.read_by_id(item_id)
    
    if not department:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return department


@router.get("/", response_model=list[Department | None], status_code=200)
def read(name: str | None = None, item_repo: Session = Depends(get_department_repo)):
    departments = item_repo.read(name=name)
    
    return departments


@router.put("/{item_id}", status_code=204)
def update(item: DepartmentCreate, item_id: int, item_repo: Session = Depends(get_department_repo)):
    response = item_repo.update(item=item, item_id=item_id)

    if response:
        return
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/{item_id}", status_code=204)
def delete(item_id: int, item_repo: Session = Depends(get_department_repo)):
    response = item_repo.delete(item_id)
    
    if response:
        return
    else: 
        raise HTTPException(status_code=404, detail="Item not found")