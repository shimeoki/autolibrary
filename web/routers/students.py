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
def read(student_id: int, student_repo: Session = Depends(get_student_repo)):
    db_student = student_repo.read(student_id)
    
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return db_student


@router.get("/", response_model=list[Student | None], status_code=200)
def read_all(student_repo: Session = Depends(get_student_repo)):
    db_book_decommision_list = student_repo.read_all()
    
    return db_book_decommision_list


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