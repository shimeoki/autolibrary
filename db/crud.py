from sqlalchemy import update
from sqlalchemy.orm import Session

from db import models, schemas
from db.password import get_hashed_password


class RepoBase:
    def __init__(self, session: Session):
        self._session = session


class BookRepo(RepoBase):
    def create(self, book: schemas.BookCreate) -> models.Book:
        session = self._session
        
        db_book = models.Book(**book.dict())
        
        session.add(db_book)
        session.commit()
        session.refresh(db_book)
        
        return db_book
    
    def read(self, book_id: int) -> models.Book | None:
        session = self._session
        
        db_book = session.get(models.Book, book_id)
        
        return db_book
  
    # def update(self):
    #     pass
    
    def delete(self, book_id: int) -> bool:
        session = self._session
        
        db_book = self.read(book_id)
        
        if not db_book:
            return False
        
        session.delete(db_book)
        session.commit()
        
        return True
        

class BookTypeRepo(RepoBase):
    def create(self, book_type: schemas.BookTypeCreate) -> models.BookType:
        session = self._session
        
        db_book_type = models.BookType(**book_type.dict())
        
        session.add(db_book_type)
        session.commit()
        session.refresh(db_book_type)
        
        return db_book_type
    
    def read(self, book_type_id: int) -> models.BookType | None:
        session = self._session
        
        db_book_type = session.get(models.BookType, book_type_id)
        
        return db_book_type
  
    def update(self, book_type: schemas.BookCreate, book_type_id: int) -> models.BookType:
        session = self._session
        
        stmt = (
            update(models.BookType)
            .where(models.BookType.id == book_type_id)
            .values(name=book_type.name)
        )
        
        session.execute(stmt)
        session.commit()
        
        db_book_type = self.read(book_type_id)
        
        return db_book_type
    
    def delete(self, book_type_id: int) -> bool:
        session = self._session
        
        db_book_type = self.read(book_type_id)
        
        if not db_book_type:
            return False
        
        session.delete(db_book_type)
        session.commit()
        
        return True
     
       
class BookGenreRepo(RepoBase):
    def create(self, book_genre: schemas.BookGenreCreate) -> models.BookGenre:
        session = self._session
        
        db_book_genre = models.BookGenre(**book_genre.dict())
        
        session.add(db_book_genre)
        session.commit()
        session.refresh(db_book_genre)
        
        return db_book_genre
    
    def read(self, book_genre_id: int) -> models.BookGenre | None:
        session = self._session
        
        db_book_genre = session.get(models.BookGenre, book_genre_id)
        
        return db_book_genre 
  
    # def update(self):
    #     pass
    
    def delete(self, book_genre_id: int) -> bool:
        session = self._session
        
        db_book_genre = self.read(book_genre_id)

        if not db_book_genre:
            return False

        session.delete(db_book_genre)
        session.commit()
        
        return True
        

class PublisherRepo(RepoBase):
    def create(self, publisher: schemas.PublisherCreate) -> models.Publisher:
        session = self._session
        
        db_publisher = models.BookType(**publisher.dict())
        
        session.add(db_publisher)
        session.commit()
        session.refresh(db_publisher)
        
        return db_publisher
    
    def read(self, publisher_id: int) -> models.Publisher | None:
        session = self._session
        
        db_publisher = session.get(models.Publisher, publisher_id)
        
        return db_publisher
  
    # def update(self):
    #     pass
    
    def delete(self, publisher_id: int) -> bool:
        session = self._session
        
        db_publisher = self.read(publisher_id)

        if not db_publisher:
            return False

        session.delete(db_publisher)
        session.commit()
        
        return True
        
        
class DepartmentRepo(RepoBase):
    def create(self, department: schemas.DepartmentCreate) -> models.Department:
        session = self._session
        
        db_department = models.BookType(**department.dict())
        
        session.add(db_department)
        session.commit()
        session.refresh(db_department)
        
        return db_department
    
    def read(self, department_id: int) -> models.Department | None:
        session = self._session
        
        db_department = session.get(models.Department, department_id)
        
        return db_department
  
    # def update(self):
    #     pass
    
    def delete(self, department_id: int) -> bool:
        session = self._session
        
        db_department = self.read(department_id)
        
        if not db_department:
            return False
        
        session.delete(db_department)
        session.commit()
        
        return True
        

class BookDecommisionRepo(RepoBase):
    def create(self, book_decommision: schemas.BookDecommisionCreate) -> models.BookDecommision:
        session = self._session
        
        db_book_decommision = models.BookDecommision(**book_decommision.dict())
        
        session.add(db_book_decommision)
        session.commit()
        session.refresh(db_book_decommision)
        
        return db_book_decommision
    
    def read(self, book_decommision_id: int) -> models.BookDecommision | None:
        session = self._session
        
        db_book_decommision = session.get(models.BookDecommision, book_decommision_id)
        
        return db_book_decommision
  
    # def update(self):
    #     pass
    
    def delete(self, book_decommision_id: int) -> bool:
        session = self._session
        
        db_book_decommision = self.read(book_decommision_id)
        
        if not db_book_decommision:
            return False

        session.delete(db_book_decommision)
        session.commit()
        
        return True
        
class StudentRepo(RepoBase):    
    def create(self, student: schemas.StudentCreate) -> models.Student:
        session = self._session
        
        hashed_password = get_hashed_password(student.password)
        
        db_student = models.Student(
            first_name=student.first_name,
            last_name=student.last_name,
            login=student.login,
            hashed_password=hashed_password
        )
        
        session.add(db_student)
        session.commit()
        session.refresh(db_student)
        
        return db_student
    
    def read(self, student_id: int) -> models.Student | None:
        session = self._session
        
        db_student = session.get(models.Student, student_id)
        
        return db_student
  
    # def update(self):
    #     pass
    
    def delete(self, student_id: int) -> bool:
        session = self._session
        
        db_student = self.read(student_id)
        
        if not db_student:
            return False
        
        session.delete(db_student)
        session.commit()
        
        return True
        

class BookStateRepo(RepoBase):
    def create(self, book_state: schemas.BookStateCreate) -> models.BookState:
        session = self._session
        
        db_book_state = models.BookState(**book_state.dict())
        
        session.add(db_book_state)
        session.commit()
        session.refresh(db_book_state)
        
        return db_book_state
    
    def read(self, book_state_id: int) -> models.BookState | None:
        session = self._session
        
        db_book_state = session.get(models.BookState, book_state_id)
        
        return db_book_state
  
    # def update(self):
    #     pass
    
    def delete(self, book_state_id: int) -> bool:
        session = self._session
        
        db_book_state = self.read(book_state_id)
        
        if not db_book_state:
            return False
        
        session.delete(db_book_state)
        session.commit()
        
        return True