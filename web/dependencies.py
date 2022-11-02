from fastapi import Depends, Request
from sqlalchemy.orm import Session

from db import crud


def get_db_session(request: Request):
    session: Session = request.app.state.session_factory()
    
    try: 
        yield session
    finally:
        session.close()
        

def get_book_repo(session: Session = Depends(get_db_session)) -> crud.BookRepo:
    return crud.BookRepo(session)

def get_book_type_repo(session: Session = Depends(get_db_session)) -> crud.BookTypeRepo:
    return crud.BookTypeRepo(session)

def get_book_genre_repo(session: Session = Depends(get_db_session)) -> crud.BookGenreRepo:
    return crud.BookGenreRepo(session)

def get_publisher_repo(session: Session = Depends(get_db_session)) -> crud.PublisherRepo:
    return crud.PublisherRepo(session)

def get_department_repo(session: Session = Depends(get_db_session)) -> crud.DepartmentRepo:
    return crud.DepartmentRepo(session)

def get_book_decommision_repo(session: Session = Depends(get_db_session)) -> crud.BookDecommisionRepo:
    return crud.BookDecommisionRepo(session)

def get_student_repo(session: Session = Depends(get_db_session)) -> crud.StudentRepo:
    return crud.StudentRepo(session)

def get_book_state_repo(session: Session = Depends(get_db_session)) -> crud.BookStateRepo:
    return crud.BookStateRepo(session)