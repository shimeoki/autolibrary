from math import ceil
from json import load

from telegram import ReplyKeyboardMarkup

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.crud import StudentRepo, BookRepo
from db.models import Student, Book


with open('D:/GitHub/.misc/tokens.json', 'r') as f:
    db_token = load(f)["db-token"]

engine = create_engine(db_token)

class BookPaginator:
    def __init__(self, lines: int, columns: int, buttons_type: int = 1, book_list: list | None = None) -> None:
        self._lines: int = lines
        self._columns: int = columns
        self._items_on_page: int = self._count_items_on_page()
        
        self._buttons_type: int = buttons_type
        
        if not book_list:
            self._items: list = self._get_items()
        else:
            self._items: list = book_list
        
        self._current_page: int = 1
        self._pages: int = self._count_pages()
    
    @property
    def current_page(self) -> int:
        return self._current_page
    
    @current_page.setter
    def current_page(self, value: int) -> None:
        if value > self.pages or value < 1:
            raise IndexError("Page out of index.")
        
        self._current_page = value
    
    @property
    def pages(self) -> int:
        return self._pages
    
    def _count_pages(self) -> int:
        items_count = len(self._items)
        pages = ceil(items_count / self._items_on_page)
        return pages
    
    @property
    def lines(self) -> int:
        return self._lines
    
    @lines.setter
    def lines(self, value: int) -> None:
        self._axis_changer(axis="line", value=value)
    
    @property
    def columns(self) -> int:
        return self._columns
    
    @columns.setter
    def columns(self, value: int) -> None:
        self._axis_changer(axis="column", value=value)
        
    def _axis_changer(self, axis: str, value: int) -> None:
        if value <= 0:
            raise ValueError("Incorrect value.")
        if axis == "line":
            self._lines = value
        elif axis == "column":
            self._columns = value

        self._items_on_page = self._count_items_on_page()
    
    def _count_items_on_page(self) -> int:
        items_on_page = self._lines * self._columns
        return items_on_page
    
    def _get_items(self) -> list:
        session = Session(engine)
        repo = BookRepo(session=session)
        
        books = repo.read()
        
        session.close()
        
        return books
    
    def _get_min_page_range(self) -> int:
        min_range = (self._current_page - 1) * self._items_on_page
        return min_range
    
    def _get_max_page_range(self) -> int:
        max_index = len(self._items)
        max_range = self._current_page * self._items_on_page
        
        if max_range > max_index:
            max_range = max_index
        
        return max_range

    def _add_buttons(self) -> list:
        if self._buttons_type == 1:
            buttons = ["<", "Фильтры", "Обратно в меню", ">"]
        else:
            buttons = ["<", "Обратно в меню", ">"]
        
        return buttons
 
    def show_page(self) -> ReplyKeyboardMarkup:
        keyboard = [[]]
        
        min_range = self._get_min_page_range()
        max_range = self._get_max_page_range()
        item_index = min_range
        
        column, line = 0, 0
        
        while line < self.lines:
            if item_index < max_range:
                item = self._items[item_index]
                keyboard[line].append(f"{item.title}\n{item.author}")
                item_index += 1
            else:
                keyboard[line].append("-")
                
            column += 1
            
            if column == self.columns:
                column = 0
                line += 1
                keyboard.append([])
        
        keyboard.append(self._add_buttons())
        
        return ReplyKeyboardMarkup(keyboard=keyboard)
    
    def page_text(self) -> str:
        text = f"Выберите предмет для просмотра.\nТекущая страница: {self._current_page}"

        return text
    
    def do_action(self, action: str) -> None:
        if action == ">" and self.current_page < self._pages:
            self.next()
        elif action == "<" and self.current_page > 1:
            self.prev()

    def next(self) -> None:
        if self.current_page >= self.pages:
            raise IndexError("Page out of index.")
        self.current_page += 1

    def prev(self) -> None:
        if self.current_page <= 1:
            raise IndexError("Page out of index.")
        self.current_page -= 1
        
    def update_book_list(self, book_list: list) -> None:
        self._items = book_list
        self._pages = self._count_pages()


class ReplyGenerator:
    def __init__(self):
        pass
    
    @staticmethod
    def menu_markup() -> ReplyKeyboardMarkup:
        keyboard = [
            ["Сделать заказ", "Корзина"],
            ["Активные книги"],
            ["Личный кабинет"],
            ["Выход"]
        ]
        
        return ReplyKeyboardMarkup(keyboard=keyboard)
        
    @staticmethod
    def profile_markup() -> ReplyKeyboardMarkup:
        keyboard = [
            ["Поменять логин"],
            ["Поменять пароль"],
            ["Обратно в меню"]
        ]
    
        return ReplyKeyboardMarkup(keyboard=keyboard)
    

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

def change_db_login(student_id: int, new_login: str) -> None:
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    repo.update_login(new_login=new_login, item_id=student_id)
    
    session.close()
    
def change_db_password(student_id: int, new_password: str) -> None:
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    repo.update_password(new_password=new_password, item_id=student_id)
    
    session.close()

def check(string: str) -> bool:
    # проверка на длину
    if not 2 <= len(string) <= 32:
        return False
    
    # проверка на символы
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ01234567890_'
    
    for i in string:
        if i not in alphabet:
            return False
    
    # прошло проверку
    return True

def check_login(login: str) -> bool:
    if not check(string=login):
        return False
    
    # проверка на уникальность
    session = Session(engine)
    repo = StudentRepo(session=session)
    
    students = repo.read()
    
    for i in students:
        if i.login == login:
            return False
    
    session.close()
    
    # прошло проверку
    return True

def check_password(password: str) -> bool:
    return check(string=password)