from sqlalchemy.orm import Session, Query
from telegram import ReplyKeyboardMarkup
from math import ceil

# сделать x и y параметры изменяемыми
class ItemPaginator:
    def __init__(self, engine, item_model) -> None:
        self._engine = engine
        self._item_model = item_model
        self._items_on_page: int = 9
        self._items: list = self._get_items()
        self._current_page: int = 1
        self._pages: int = self._count_pages()
    
    @property
    def current_page(self) -> int:
        return self._current_page
    
    @current_page.setter
    def current_page(self, value: int) -> None:
        if value > self._pages:
            raise IndexError("Page out of index.")
        elif value < 1:
            raise IndexError("Page out of index.")
        self._current_page = value
    
    @property
    def pages(self) -> int:
        return self._pages
    
    def _get_items(self) -> list:
        with Session(self._engine) as session:
            query = session.query(self._item_model)
            return query.all()    

    def _count_pages(self) -> int:
        items_count = len(self._items)
        pages = ceil(items_count / self._items_on_page)
        return pages
    
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
 
    def page(self) -> ReplyKeyboardMarkup:
        keyboard = [[]]
        
        min_range = self._get_min_page_range()
        max_range = self._get_max_page_range()
        
        x, y = 0, 0
        
        for item in self._items[min_range:max_range]:
            if x > 2:
                x = 0
                y += 1
                keyboard.append([])
            
            keyboard[y].append(item.name)
            x += 1
        
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


class SyncOrder:
    def __init__(self,
                 engine,
                 order_model,
                 order_item_model,
                 employee_model, # убрать employee
                 total_price: int,
                 qrcode_id: int,
                 current_order: list
    ) -> None:
        self._engine = engine
        self._order_model = order_model
        self._order_item_model = order_item_model
        self._employee_model = employee_model
        self._total_price = total_price
        self._qrcode_id = qrcode_id
        self._current_order = current_order
        
        self._order = self._make_order()
        self._order_items = self._make_order_items()

    def _make_order(self):
        getter = ItemGetter(engine=self._engine, item_model=self._order_model)
        order_id = getter.get_new_id()
        
        order = self._order_model(
            id=order_id,
            ready=False,
            total_price=self._total_price,
            client_id=None,
            employee_id=self._get_employee_id()
        )
        
        self._increment_employee_orders(employee_id=order.employee_id)
        
        return order
        
    def _get_employee_id(self) -> int:
        getter = ItemGetter(engine=self._engine, item_model=self._employee_model)
        query = getter._query
        query = query.order_by(self._employee_model.order_count).first()
        return query.id
    
    def _increment_employee_orders(self, employee_id) -> None:
        with Session(self._engine) as session:
            query = session.query(self._employee_model).filter(self._employee_model.id == employee_id)
            orders = query.one().order_count
            query.update({"order_count": orders+1}, synchronize_session="fetch")
    
    def _make_order_items(self) -> list:
        order_items = []
        
        getter = ItemGetter(engine=self._engine, item_model=self._order_item_model)
        order_item_id = getter.get_new_id()
        
        for item_id in self._current_order:
            order_item = self._order_item_model(
                id=order_item_id,
                order_id=self._order.id,
                item_id=item_id
            )
            
            order_items.append(order_item)
            order_item_id += 1
            
        return order_items
    
    def commit(self) -> None:
        with Session(self._engine) as session:
            session.add(self._order)
            session.add_all(self._order_items)
            
            session.commit()