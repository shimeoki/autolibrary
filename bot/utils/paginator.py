from math import ceil

from telegram import ReplyKeyboardMarkup
from sqlalchemy.orm import Session

from db.crud import BookRepo
from bot.engine import engine

"""
Данный класс предназначен для пагинации книг из базы данных или произвольного списка.
При инициализации класса необходимо указать количество рядов и столбцов на каждой странице (без учёта нижнего ряда).
Предполагается, что вручную можно изменять количество рядов/столбцов, текущую страницу и массив с книгами.
Страницы выводятся через класс ReplyKeyboardMarkup (wrapper python-telegram-bot) для отображения в телеграме через клавиатуру в чате.
"""
class Paginator:
    def __init__(self, rows: int, columns: int, additional_button: str | None = None, book_list: list | None = None) -> None:
        # ряды и столбцы для одной страницы без учёта нижнего ряда с кнопками
        self._rows: int = rows
        self._columns: int = columns
        
        # количество книг на одной странице для корректной работы цикла
        self._books_on_page: int = self._count_books_on_page()
        
        # дополнительная кнопка в нижнем ряду с текстом по желанию
        self._additional_button: str | None = additional_button
        
        # book_list - массив с книгами, который можно использовать, если не нужно получать книги из базы данных
        if not book_list:
            self._books: list = self._get_books()
        else:
            self._books: list = book_list
        
        # текущая страница для отображения и общее кол-во страниц для лимитирования перелистывания
        self._current_page: int = 1
        self._pages: int = self._count_pages()
    
    
    # текущая страница
    @property
    def current_page(self) -> int:
        return self._current_page
    
    # данная функция вызовется, если попытаться поменять текущую страницу вручную
    @current_page.setter
    def current_page(self, value: int) -> None:
        # проверка, чтобы можно было всегда показать первую страницу, даже если книг нет
        if value == 1:
            pass
        # проверка на превышение общего возможного количества страниц или неположительное значение
        elif value > self.pages or value < 1:
            raise IndexError("Page out of index.")
        
        self._current_page = value
    
    # общее кол-во страниц
    @property
    def pages(self) -> int:
        return self._pages
    
    # доп. функция для подсчёта общего кол-ва страниц
    def _count_pages(self) -> int:
        return ceil(len(self._books) / self._books_on_page)
    
    # ряды
    @property
    def rows(self) -> int:
        return self._rows
    
    # данная функция вызовется, если попытаться поменять количество рядов вручную
    @rows.setter
    def rows(self, value: int) -> None:
        self._axis_changer(axis="row", value=value)
    
    # столбцы
    @property
    def columns(self) -> int:
        return self._columns
    
    # данная функция вызовется, если попытаться поменять количество столбцов вручную
    @columns.setter
    def columns(self, value: int) -> None:
        self._axis_changer(axis="column", value=value)
    
    # доп. функция для смены кол-ва рядов/столбцов в целях сокращения строк кода 
    def _axis_changer(self, axis: str, value: int) -> None:
        # проверка на неположительное значение
        if value <= 0:
            raise ValueError("Incorrect value.")
        
        # изменение кол-ва рядов/столбцов в зависимости от параметра axis
        if axis == "row":
            self._rows = value
        elif axis == "column":
            self._columns = value
            
        # подсчёт кол-ва книг на странице заново
        self._books_on_page = self._count_books_on_page()
    
    # функция для подсчёта кол-ва книг на странице
    def _count_books_on_page(self) -> int:
        return self.rows * self.columns
    
    # получение доступных книг из базы данных и их фильтрация по названию/автору при надобности
    def _get_books(self, title: str | None = None, author: str | None = None) -> list:
        # получение репозитория для проведения операций с таблицей книг
        session = Session(engine)
        repo = BookRepo(session=session)
        
        # получение нужных книг
        books = repo.search_available(title=title, author=author)
        
        # закрытие сессии
        session.close()
        
        return books
    
    # минимальный индекс для книг на текущей странице
    def _get_min_page_range(self) -> int:
        return (self.current_page - 1) * self._books_on_page
    
    # максимальный индекс для книг на текущей странице
    def _get_max_page_range(self) -> int:
        # эта проверка необходима, если максимальный индекс книг меньше, чем максимально возможный индекс на странице
        max_index = len(self._books)
        max_range = self.current_page * self._books_on_page
        
        if max_range > max_index:
            max_range = max_index
        
        return max_range

    # нижний ряд кнопок
    def _add_buttons(self) -> list:
        # добавление дополнительной кнопки при наличии
        if self._additional_button:
            buttons = ["<", self._additional_button, "Обратно в меню", ">"]
        else:
            buttons = ["<", "Обратно в меню", ">"]
        
        return buttons

    # метод для отображения страницы
    def show_page(self) -> ReplyKeyboardMarkup:
        keyboard = [[]]
        
        # минимальный и максимальный индексы
        min_range = self._get_min_page_range()
        max_range = self._get_max_page_range()
        book_index = min_range # первая книга равна минимальному индексу
        
        row, column = 0, 0
        
        # основной цикл
        while row < self.rows:
            if book_index < max_range: # пока есть книги для отображения
                book = self._books[book_index]
                keyboard[row].append(f"{book.title}\n{book.author}")
                book_index += 1
            else: # заполнение пустого места дефисами
                keyboard[row].append("-")
            
            # следующий столбец
            column += 1
            
            # если дошли до последнего столбца, то переходим на следующий ряд
            if column == self.columns:
                column = 0
                row += 1
                keyboard.append([])
        
        # нижний ряд кнопок по окончанию цикла
        keyboard.append(self._add_buttons())
        
        return ReplyKeyboardMarkup(keyboard=keyboard)
    
    # текст с текущей страницей для отображения в чате
    def page_text(self) -> str:
        return f"Выберите предмет для просмотра.\nТекущая страница: {self.current_page}"
    
    # если происходит нажатие на одну из кнопок для переключение страницы
    def do_action(self, action: str) -> None:
        # если переходим на следующую, проверка на максимальное кол-во страниц
        if action == ">" and self.current_page < self.pages:
            self.next_page()
        # если переходим на предыдущую, проверка на первую страницу
        elif action == "<" and self.current_page > 1:
            self.previous_page()

    # переключение на следующую страницу
    def next_page(self) -> None:
        # проверка на максимальное кол-во страниц
        if self.current_page >= self.pages:
            raise IndexError("Page out of index.")
        self.current_page += 1
    
    # переключение на предыдущую страницу
    def previous_page(self) -> None:
        # проверка на первую страницу
        if self.current_page <= 1:
            raise IndexError("Page out of index.")
        self.current_page -= 1
    
    # метод для обновления массива книг списком из аргумента
    def update_book_list(self, book_list: list) -> None:
        self._books = book_list
        self._pages = self._count_pages()
    
    # метод для обновления книг из базы данных
    def update_books(self, title: str | None = None, author: str | None = None) -> None:
        self._books = self._get_books(title=title, author=author)
        self._pages = self._count_pages()