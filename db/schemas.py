from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    author: str
    series: str | None = None
    page_total: int
    publication_year: str = Field(min_length=4, max_length=4)
    receipt_year: str = Field(min_length=4, max_length=4)
    price: float | None = None
    isbn: str | None = Field(default=None, min_length=17, max_length=17)
    bbk: str | None = Field(default=None, max_length=32)
    receive_date: date | None = None # поставить отдельный класс для даты
    return_date: date | None = None  # ^ ^ ^
    

class BookCreate(BookBase):
    type_id: int
    genre_id: int | None = None
    publisher_id: int
    department_id: int
    decommision_id: int | None = None
    student_id: int
    state_id: int


class Book(BookBase):
    id: int
    type: BookType
    genre: BookGenre | None = None
    publisher: Publisher
    department: Department
    decommision: BookDecommision | None = None
    student: Student
    state: BookState
    
    class Config:
        orm_mode = True


class BookTypeBase(BaseModel):
    name: str
    

class BookTypeCreate(BookTypeBase):
    pass


class BookType(BookTypeBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
        
class BookGenreBase(BaseModel):
    name: str
    

class BookGenreCreate(BookGenreBase):
    pass


class BookGenre(BookGenreBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
        
class PublisherBase(BaseModel):
    name: str
    city: str
    

class PublisherCreate(PublisherBase):
    pass


class Publisher(PublisherBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
        
class DepartmentBase(BaseModel):
    name: str
    

class DepartmentCreate(DepartmentBase):
    pass


class Department(DepartmentBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
    
class BookDecommisionBase(BaseModel):
    books_total: int
    

class BookDecommisionCreate(BookDecommisionBase):
    pass


class BookDecommision(BookDecommisionBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
    
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    login: str
    

class StudentCreate(StudentBase):
    password: str
    
    
class Student(StudentBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        
    
class BookStateBase(BaseModel):
    name: str


class BookStateCreate(BookStateBase):
    pass


class BookState(BookStateBase):
    id: int
    books: list[Book] = []
    
    class Config:
        orm_mode = True
        

Book.update_forward_refs()