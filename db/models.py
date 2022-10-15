from sqlalchemy import Column, String, Integer, ForeignKey, SmallInteger, Numeric
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Students(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    login = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    

class Books(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    type_id = Column(SmallInteger, ForeignKey("book_types.id"), nullable=False)
    title = Column(String(64), nullable=False)
    author = Column(String(64), nullable=False)
    series = Column(String(64))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    page_total = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    publication_year = Column(String(4), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    receipt_year = Column(String(4), nullable=False)
    price = Column(Numeric(19, 4))
    isbn = Column(String(17))
    bbk = Column(String(32))
    decommision_id = Column(Integer, ForeignKey("decommisions.id"))
    
    
class UsageHistory(Base):
    __tablename__ = "usage_history"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    

class BookTypes(Base):
    __tablename__ = "book_types"
    
    id = Column(SmallInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    

class Decommisions(Base):
    __tablename__ = "decommisions"
    
    id = Column(Integer, primary_key=True)
    books_total = Column(Integer, nullable=False)
    

class Departments(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    

class Genres(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(32), nullable=False)
    
    
class Publishers(Base):
    __tablename__ = "publishers"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    city = Column(String(16), nullable=False)