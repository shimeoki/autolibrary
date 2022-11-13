from fastapi import Depends, Request
from sqlalchemy.orm import Session

from db.crud import (
    BookRepo, 
    BookTypeRepo, 
    BookGenreRepo, 
    PublisherRepo, 
    DepartmentRepo, 
    BookDecommisionRepo, 
    StudentRepo, 
    BookStateRepo
)


def get_db_session(request: Request):
    session: Session = request.app.state.session_factory()
    
    try: 
        yield session
    finally:
        session.close()
        

def get_book_repo(session: Session = Depends(get_db_session)) -> BookRepo:
    return BookRepo(session)

def get_book_type_repo(session: Session = Depends(get_db_session)) -> BookTypeRepo:
    return BookTypeRepo(session)

def get_book_genre_repo(session: Session = Depends(get_db_session)) -> BookGenreRepo:
    return BookGenreRepo(session)

def get_publisher_repo(session: Session = Depends(get_db_session)) -> PublisherRepo:
    return PublisherRepo(session)

def get_department_repo(session: Session = Depends(get_db_session)) -> DepartmentRepo:
    return DepartmentRepo(session)

def get_book_decommision_repo(session: Session = Depends(get_db_session)) -> BookDecommisionRepo:
    return BookDecommisionRepo(session)

def get_student_repo(session: Session = Depends(get_db_session)) -> StudentRepo:
    return StudentRepo(session)

def get_book_state_repo(session: Session = Depends(get_db_session)) -> BookStateRepo:
    return BookStateRepo(session)