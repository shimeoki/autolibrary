from typing import Optional
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
    series: Mapped[Optional[str]]
    genre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("book_genres.id"))
    page_total: Mapped[int]
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))
    publication_year: Mapped[str] = mapped_column(String(4))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    receipt_year: Mapped[str] = mapped_column(String(4))
    price: Mapped[Optional[float]] = mapped_column(Numeric(19, 4))
    isbn: Mapped[Optional[str]] = mapped_column(String(17))
    bbk: Mapped[Optional[str]]
    decommision_id: Mapped[Optional[int]] = mapped_column(ForeignKey("book_decommisions.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    state_id: Mapped[int] = mapped_column(ForeignKey("book_states.id"))
    receive_date: Mapped[Optional[date]] = mapped_column(String(10))
    return_date: Mapped[Optional[date]] = mapped_column(String(10))
    
    type: Mapped["BookType"] = relationship(back_populates="books")
    genre: Mapped["BookGenre"] = relationship(back_populates="books")
    publisher: Mapped["Publisher"] = relationship(back_populates="books")
    department: Mapped["Department"] = relationship(back_populates="books")
    decommision: Mapped["BookDecommision"] = relationship(back_populates="books")
    student: Mapped["Student"] = relationship(back_populates="books")
    state: Mapped["BookState"] = relationship(back_populates="books")


class BookType(Base):
    __tablename__ = "book_types"
    
    name: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="type")


class BookGenre(Base):
    __tablename__ = "book_genres"
    
    name: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="genre")


class Publisher(Base):
    __tablename__ = "publishers"
    
    name: Mapped[str]
    city: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="publisher")
    

class Department(Base):
    __tablename__ = "departments"
    
    name: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="department")


class BookDecommision(Base):
    __tablename__ = "book_decommisions"
    
    books_total: Mapped[int]
    
    books: Mapped[list[Book]] = relationship(back_populates="decommision")


class Student(Base):
    __tablename__ = "students"
    
    first_name: Mapped[str]
    last_name: Mapped[str]
    login: Mapped[str]
    hashed_password: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="student")

  
class BookState(Base):
    __tablename__ = "book_states"
    
    name: Mapped[str]
    
    books: Mapped[list[Book]] = relationship(back_populates="state")