from sqlalchemy.orm import Session, Query
from telegram import ReplyKeyboardMarkup
from math import ceil

class ItemPaginator:
    def __init__(self,
                 engine, 
                item_model,
                lines: int,
                columns: int) -> None:
        self._engine = engine
        self._item_model = item_model
        
        self._lines: int = lines
        self._columns: int = columns
        self._items_on_page: int = self._count_items_on_page()
        
        self._items: list = self._get_items()
        
        self._current_page: int = 1
        self._pages: int = self._count_pages()
    
    @property
    def current_page(self) -> int:
        return self._current_page
    
    @current_page.setter
    def current_page(self, value: int) -> None:
        if value > self._pages or value < 1:
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
        with Session(self._engine) as session:
            query = session.query(self._item_model)
            return query.all()
    
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
        buttons = ["<", "Обратно в меню", ">"]
        return buttons
 
    def show_page(self) -> ReplyKeyboardMarkup:
        keyboard = [[]]
        
        min_range = self._get_min_page_range()
        max_range = self._get_max_page_range()
        
        column, line = 0, 0
        
        for item in self._items[min_range:max_range]:
            if column == self._columns:
                column = 0
                line += 1
                keyboard.append([])
            
            keyboard[line].append(item.title)
            column += 1
        
        keyboard.append(self._add_buttons())
        
        return ReplyKeyboardMarkup(keyboard=keyboard)
    
    def page_text(self) -> str:
        text = f"Выберите предмет для просмотра.\nТекущая страница: {self._current_page}"

        return text
    
    def do_action(self, action: str) -> None:
        if action == ">" and self._current_page != self._pages:
            self.next()
        elif action == "<" and self._current_page != 1:
            self.prev()

    def next(self) -> None:
        if self._current_page == self._pages:
            raise IndexError("Page out of index.")
        self._current_page += 1

    def prev(self) -> None:
        if self._current_page == 1:
            raise IndexError("Page out of index.")
        self._current_page -= 1


class ItemGetter:
    def __init__(self, engine, item_model) -> None:
        self._engine = engine
        self._item_model = item_model
        
        self._query = self._get_query()
    
    def _get_query(self) -> Query:
        with Session(self._engine) as session:
            query = session.query(self._item_model)
            return query
        
    def get_query_list(self) -> list:
        return self._query.all()
    
    def get_item(self, attribute: str, value):
        query = self._query
        result = query.filter(self._item_model.__dict__[attribute] == value).one_or_none()
        return result
    
    def get_new_id(self) -> int:
        query = self._query.order_by(self._item_model.id).all()
        
        if not query:
            return 1
        
        last_id = query[-1].id
        return last_id + 1
            

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