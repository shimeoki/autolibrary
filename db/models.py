from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger, Numeric, DATE
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    
    id: int = Column(Integer, primary_key=True)
    type_id: int = Column(SmallInteger, ForeignKey("book_types.id"), nullable=False)
    title: str = Column(String(64), nullable=False)
    author: str = Column(String(64), nullable=False)
    series: str = Column(String(64))
    genre_id: int = Column(Integer, ForeignKey("book_genres.id"))
    page_total: int = Column(Integer, nullable=False)
    publisher_id: int = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    publication_year: str = Column(String(4), nullable=False)
    department_id: int = Column(Integer, ForeignKey("departments.id"), nullable=False)
    receipt_year: str = Column(String(4), nullable=False)
    price: float = Column(Numeric(19, 4))
    isbn: str = Column(String(17))
    bbk: str = Column(String(32))
    decommision_id: int = Column(Integer, ForeignKey("book_decommisions.id"))
    student_id: int = Column(Integer, ForeignKey("students.id"), nullable=False)
    state_id: int = Column(SmallInteger, ForeignKey("book_states.id"), nullable=False)
    receive_date: str = Column(DATE)
    return_date: str = Column(DATE)
    
    type: "BookType" = relationship("BookType", back_populates="books")
    genre: "BookGenre" = relationship("BookGenre", back_populates="books")
    publisher: "Publisher" = relationship("Publisher", back_populates="books")
    department: "Department" = relationship("Department", back_populates="books")
    decommision: "BookDecommision" = relationship("BookDecommision", back_populates="books")
    student: "Student" = relationship("Student", back_populates="books")
    state: "BookState" = relationship("BookState", back_populates="books")


class BookType(Base):
    __tablename__ = "book_types"
    
    id: int = Column(SmallInteger, primary_key=True)
    name: str = Column(String(32), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="type")


class BookGenre(Base):
    __tablename__ = "book_genres"
    
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(32), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"
    
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(64), nullable=False)
    city: str = Column(String(16), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="publisher")
    

class Department(Base):
    __tablename__ = "departments"
    
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(32), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="department")


class BookDecommision(Base):
    __tablename__ = "book_decommisions"
    
    id: int = Column(Integer, primary_key=True)
    books_total: int = Column(Integer, nullable=False)
    
    books: "Book" = relationship("Book", back_populates="decommision")


class Student(Base):
    __tablename__ = "students"
    
    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(32), nullable=False)
    last_name: str = Column(String(32), nullable=False)
    login: str = Column(String(32), nullable=False)
    password: str = Column(String(32), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="student")

  
class BookState(Base):
    __tablename__ = "book_states"
    
    id: int = Column(SmallInteger, primary_key=True)
    name: str = Column(String(32), nullable=False)
    
    books: "Book" = relationship("Book", back_populates="state")