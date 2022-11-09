from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from web.dependencies import get_student_repo
from db.schemas import Student, StudentCreate


router = APIRouter()


@router.post("/", response_model=Student, status_code=201)
def create(student: StudentCreate, student_repo: Session = Depends(get_student_repo)):
    db_student = student_repo.create(student)
    
    return db_student


@router.get("/{student_id}", response_model=Student, status_code=200)
def read_by_id(student_id: int, student_repo: Session = Depends(get_student_repo)):
    db_student = student_repo.read_by_id(student_id)
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return db_student


@router.get("/", response_model=list[Student | None], status_code=200)
def read(first_name: str | None = None,
         last_name: str | None = None,
         login: str | None = None,
         student_repo: Session = Depends(get_student_repo)
):
    db_student_list = student_repo.read(first_name=first_name, last_name=last_name, login=login)
    
    return db_student_list


@router.put("/{student_id}", status_code=200)
def update(student: StudentCreate, student_id: int, student_repo: Session = Depends(get_student_repo)):
    student_repo.update(student=student, student_id=student_id)

    return {"status code": 200}


@router.delete("/{student_id}", status_code=200)
def delete(student_id: int, student_repo: Session = Depends(get_student_repo)):
    db_response = student_repo.delete(student_id)
    
    if not db_response:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {"status code": 200}