from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_department_repo
from db.schemas import Department, DepartmentCreate


router = APIRouter()


@router.post("/", response_model=Department, status_code=201)
def create(department: DepartmentCreate, department_repo: Session = Depends(get_department_repo)):
    db_department = department_repo.create(department)
    
    return db_department


@router.get("/{department_id}", response_model=Department, status_code=200)
def read_by_id(department_id: int, department_repo: Session = Depends(get_department_repo)):
    db_department = department_repo.read_by_id(department_id)
    
    if not db_department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return db_department


@router.get("/", response_model=list[Department | None], status_code=200)
def read(name: str | None = None, department_repo: Session = Depends(get_department_repo)):
    db_department_list = department_repo.read(name)
    
    return db_department_list


@router.put("/{department_id}", status_code=200)
def update(department: DepartmentCreate, department_id: int, department_repo: Session = Depends(get_department_repo)):
    department_repo.update(department=department, department_id=department_id)

    return {"status code": 200}


@router.delete("/{department_id}", status_code=200)
def delete(department_id: int, department_repo: Session = Depends(get_department_repo)):
    db_response = department_repo.delete(department_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {"status code": 200}