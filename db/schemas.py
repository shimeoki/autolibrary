from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    series: str | None
    page_total: int
    publication_year: str # поставить отдельный класс для года
    receipt_year: str     # ^ ^ ^
    price: float | None
    isbn: str | None # поставить отдельный класс для ISBN
    bbk: str | None  # поставить отдельный класс для BBK
    receive_date: str | None # поставить отдельный класс для даты
    return_date: str | None  # ^ ^ ^
    

class BookCreate(BookBase):
    type_id: int
    genre_id: int | None
    publisher_id: int
    department_id: int
    decommision_id: int | None
    student_id: int
    state_id: int


class Book(BookBase):
    id: int
    
    class Config:
        orm_mode = True