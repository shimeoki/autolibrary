from __future__ import annotations
from datetime import date

from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Book(Base):
    __tablename__ = "books"
    
    type_id: Mapped[int] = mapped_column(ForeignKey("book_types.id"))
    title: Mapped[str]
    author: Mapped[str]
    series: Mapped[str | None]
    genre_id: Mapped[int | None] = mapped_column(ForeignKey("book_genres.id"))
    page_total: Mapped[int]
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publication_year: Mapped[str] = mapped_column(String(4))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    receipt_year: Mapped[str] = mapped_column(String(4))
    price: Mapped[float | None] = mapped_column(Numeric(19, 4))
    isbn: Mapped[str | None] = mapped_column(String(17))
    bbk: Mapped[str | None]
    decommision_id: Mapped[int | None] = mapped_column(ForeignKey("book_decommisions.id"))
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    state_id: Mapped[int] = mapped_column(ForeignKey("book_states.id"))
    receive_date: Mapped[date | None] = mapped_column(String(10))
    return_date: Mapped[date | None] = mapped_column(String(10))
    
    type: Mapped[BookType] = relationship()
    genre: Mapped[BookGenre] = relationship()
    publisher: Mapped[Publisher] = relationship()
    department: Mapped[Department] = relationship()
    decommision: Mapped[BookDecommision] = relationship()
    student: Mapped[Student] = relationship()
    state: Mapped[BookState] = relationship()


class BookType(Base):
    __tablename__ = "book_types"
    
    name: Mapped[str]


class BookGenre(Base):
    __tablename__ = "book_genres"
    
    name: Mapped[str]


class Publisher(Base):
    __tablename__ = "publishers"
    
    name: Mapped[str]
    city: Mapped[str]
    

class Department(Base):
    __tablename__ = "departments"
    
    name: Mapped[str]


class BookDecommision(Base):
    __tablename__ = "book_decommisions"
    
    books_total: Mapped[int]


class Student(Base):
    __tablename__ = "students"
    
    first_name: Mapped[str]
    last_name: Mapped[str]
    login: Mapped[str]
    hashed_password: Mapped[str]

  
class BookState(Base):
    __tablename__ = "book_states"
    
    name: Mapped[str]