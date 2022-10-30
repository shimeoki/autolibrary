from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger, Numeric, DATE
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    type_id = Column(SmallInteger, ForeignKey("book_types.id"), nullable=False)
    title = Column(String(64), nullable=False)
    author = Column(String(64), nullable=False)
    series = Column(String(64))
    genre_id = Column(Integer, ForeignKey("book_genres.id"))
    page_total = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    publication_year = Column(String(4), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    receipt_year = Column(String(4), nullable=False)
    price = Column(Numeric(19, 4))
    isbn = Column(String(17))
    bbk = Column(String(32))
    decommision_id = Column(Integer, ForeignKey("book_decommisions.id"))
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    state_id = Column(SmallInteger, ForeignKey("book_states.id"), nullable=False)
    receive_date = Column(DATE)
    return_date = Column(DATE)
    
    type = relationship("BookType", back_populates="books")
    genre = relationship("BookGenre", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    department = relationship("Department", back_populates="books")
    decommision = relationship("BookDecommision", back_populates="books")
    student = relationship("Student", back_populates="books")
    state = relationship("BookState", back_populates="books")


class BookType(Base):
    __tablename__ = "book_types"
    
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    
    books = relationship("Book", back_populates="type")


class BookGenre(Base):
    __tablename__ = "book_genres"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    
    books = relationship("Book", back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    city = Column(String(16), nullable=False)
    
    books = relationship("Book", back_populates="publisher")
    

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    
    books = relationship("Book", back_populates="department")


class BookDecommision(Base):
    __tablename__ = "book_decommisions"
    
    id = Column(Integer, primary_key=True)
    books_total = Column(Integer, nullable=False)
    
    books = relationship("Book", back_populates="decommision")


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    login = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    
    books = relationship("Book", back_populates="student")

  
class BookState(Base):
    __tablename__ = "book_states"
    
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    
    books = relationship("Book", back_populates="state")