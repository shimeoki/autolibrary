from telegram import ReplyKeyboardMarkup


def menu_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        ["Магазин"],
        ["Корзина"],
        ["Инвентарь"],
        ["Личный кабинет"]
    ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard)
        

def profile_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        ["Поменять логин"],
        ["Поменять пароль"],
        ["Обратно в меню"],
        ["Выход"]
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard)
    

def inventory_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        ["В обработке"],
        ["Для выдачи"],
        ["На руках"],
        ["Обратно в меню"]
    ]
        
    return ReplyKeyboardMarkup(keyboard=keyboard)
    

def changing_credentials_markup() -> ReplyKeyboardMarkup:
    keyboard = [
        ["Обратно в меню"]
    ]
        
    return ReplyKeyboardMarkup(keyboard=keyboard)
    

def filters_markup(title: str | None = None, author: str | None = None) -> ReplyKeyboardMarkup:
    title = f"Название:\n{title}"
    author = f"Автор:\n{author}"
        
    keyboard = [
        [title],
        [author],
        ["Обратно в магазин"]
    ]
        
    return ReplyKeyboardMarkup(keyboard=keyboard)