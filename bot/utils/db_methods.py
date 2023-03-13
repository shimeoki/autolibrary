from sqlalchemy.orm import Session

from db.crud import StudentRepo, BookRepo
from db.models import Student, Book
from bot.engine import engine


def reserve_book(student_id: int, book_id: int) -> bool:
    session = Session(engine)
    repo = BookRepo(session=session)
    
    result = repo.update(student_id=student_id, item_id=book_id)
    
    return result


def get_inventory_books(student_id: int, state_name: str) -> list[Book | None]:
    session = Session(engine)
    repo = BookRepo(session=session)
    
    books = repo.read(student_id=student_id, state_name=state_name)
    
    session.close()
    
    return books


def get_student(login: str) -> Student | None:
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    student = repo.read(login=login)
    
    session.close()
    
    if not student:
        return None
    else:
        return student[0]


def get_book(title: str, author: str) -> Book | None:
    session = Session(engine)
    repo = BookRepo(session=session)
    
    book = repo.read(title=title, author=author)
    
    session.close()
    
    if not book:
        return None
    else:
        return book[0]
    
    
def get_book_by_id(book_id: int) -> Book | None:
    session = Session(engine)
    repo = BookRepo(session=session)
    
    book = repo.read_by_id(item_id=book_id)
    
    session.close()
    
    if not book:
        return None
    else:
        return book