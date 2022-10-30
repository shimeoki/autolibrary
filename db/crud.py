from sqlalchemy.orm import Session

from db import models, schemas


# отдельный класс RepoBase чтобы не прописывать __init__


class BookRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, book: schemas.BookCreate) -> models.Book:
        db_book = models.Book(**book.dict())
        
        session = self._session
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        
        return db_book
    
    def read(self, book_id: int) -> models.Book:
        session = self._session
        
        return session.get(models.Book, book_id)
  
    # def update(self):
    #     pass
    
    def delete(self, book_id: int) -> None:
        db_book = self.read(book_id)
        
        session = self._session
        session.delete(db_book)
        session.commit()
        

class BookTypeRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, book_type: schemas.BookTypeCreate) -> models.BookType:
        db_book_type = models.BookType(**book_type.dict())
        
        session = self._session
        session.add(db_book_type)
        session.commit()
        session.refresh(db_book_type)
        
        return db_book_type
    
    def read(self, book_type_id: int) -> models.BookType:
        session = self._session
        
        return session.get(models.BookType, book_type_id)
  
    # def update(self):
    #     pass
    
    def delete(self, book_type_id: int) -> None:
        db_book_type = self.read(book_type_id)
        
        session = self._session
        session.delete(db_book_type)
        session.commit()
        
        
class BookGenreRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, book_genre: schemas.BookGenreCreate) -> models.BookGenre:
        db_book_genre = models.BookGenre(**book_genre.dict())
        
        session = self._session
        session.add(db_book_genre)
        session.commit()
        session.refresh(db_book_genre)
        
        return db_book_genre
    
    def read(self, book_genre_id: int) -> models.BookGenre:
        session = self._session
        
        return session.get(models.BookGenre, book_genre_id)
  
    # def update(self):
    #     pass
    
    def delete(self, book_genre_id: int) -> None:
        db_book_genre = self.read(book_genre_id)
        
        session = self._session
        session.delete(db_book_genre)
        session.commit()
        
        
class PublisherRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, publisher: schemas.PublisherCreate) -> models.Publisher:
        db_publisher = models.BookType(**publisher.dict())
        
        session = self._session
        session.add(db_publisher)
        session.commit()
        session.refresh(db_publisher)
        
        return db_publisher
    
    def read(self, publisher_id: int) -> models.Publisher:
        session = self._session
        
        return session.get(models.Publisher, publisher_id)
  
    # def update(self):
    #     pass
    
    def delete(self, publisher_id: int) -> None:
        db_publisher = self.read(publisher_id)
        
        session = self._session
        session.delete(db_publisher)
        session.commit()
        
        
class DepartmentRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, department: schemas.DepartmentCreate) -> models.Department:
        db_department = models.BookType(**department.dict())
        
        session = self._session
        session.add(db_department)
        session.commit()
        session.refresh(db_department)
        
        return db_department
    
    def read(self, department_id: int) -> models.Department:
        session = self._session
        
        return session.get(models.Department, department_id)
  
    # def update(self):
    #     pass
    
    def delete(self, department_id: int) -> None:
        db_department = self.read(department_id)
        
        session = self._session
        session.delete(db_department)
        session.commit()
        

class BookDecommisionRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, book_decommision: schemas.BookDecommisionCreate) -> models.BookDecommision:
        db_book_decommision = models.BookDecommision(**book_decommision.dict())
        
        session = self._session
        session.add(db_book_decommision)
        session.commit()
        session.refresh(db_book_decommision)
        
        return db_book_decommision
    
    def read(self, book_decommision_id: int) -> models.BookDecommision:
        session = self._session
        
        return session.get(models.BookDecommision, book_decommision_id)
  
    # def update(self):
    #     pass
    
    def delete(self, book_decommision_id: int) -> None:
        db_book_decommision = self.read(book_decommision_id)
        
        session = self._session
        session.delete(db_book_decommision)
        session.commit()
        
        
class StudentRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, student: schemas.StudentCreate) -> models.Student:
        db_student = models.Student(**student.dict())
        
        session = self._session
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        
        return db_student
    
    def read(self, student_id: int) -> models.Student:
        session = self._session
        
        return session.get(models.Student, student_id)
  
    # def update(self):
    #     pass
    
    def delete(self, student_id: int) -> None:
        db_student = self.read(student_id)
        
        session = self._session
        session.delete(db_student)
        session.commit()
        

class BookStateRepo:
    def __init__(self, session: Session):
        self._session = session
        
    def create(self, book_state: schemas.BookStateCreate) -> models.BookState:
        db_book_state = models.BookState(**book_state.dict())
        
        session = self._session
        session.add(db_book_state)
        session.commit()
        session.refresh(db_book_state)
        
        return db_book_state
    
    def read(self, book_state_id: int) -> models.BookState:
        session = self._session
        
        return session.get(models.BookState, book_state_id)
  
    # def update(self):
    #     pass
    
    def delete(self, book_state_id: int) -> None:
        db_book_state = self.read(book_state_id)
        
        session = self._session
        session.delete(db_book_state)
        session.commit()