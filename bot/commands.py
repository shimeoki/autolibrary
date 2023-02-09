from telegram import Update
from telegram.ext import ContextTypes

from db.models import (
    Book
)

from bot.utils import (
    ReplyGenerator,
    ItemPaginator,
    change_db_login,
    change_db_password,
    check_login,
    check_password,
    get_student
)

from db.password import verify_password

LOGIN, PASSWORD, MENU, SHOP, PROFILE, CHANGE_LOGIN, CHANGE_PASSWORD = range(7)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    user_data["student"] = None
    user_data["login_status"] = None
    user_data["inventory"] = []
    user_data["basket"] = []    
    user_data["shop_paginator"] = ItemPaginator(
        item_model=Book,
        lines=3,
        columns=3
    )
    
    await update.message.reply_text(
        text="Привет! Введи свой логин, чтобы продолжить."
    )
    
    return LOGIN


async def enter_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    login = update.message.text
    
    student = get_student(login=login)
    
    if not student:
        await update.message.reply_text(
            text="Логин неверный, попробуйте ещё раз."
        )

        return LOGIN

    user_data["student"] = student
    
    await update.message.reply_text(
        text="Введите пароль."
    )
    
    return PASSWORD


async def enter_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    password = update.message.text
    
    student = user_data["student"]
    
    verify = verify_password(password, student.hashed_password)
    
    if not verify:
        await update.message.reply_text(
            text="Пароль неверный, попробуйте ещё раз."
        )

        return LOGIN

    user_data["login_status"] = True
    
    text = f"Добро пожаловать, {student.last_name} {student.first_name}!"
    
    await update.message.reply_text(
        text=text,
        reply_markup=ReplyGenerator.menu_markup()
    )
    
    return MENU


async def show_shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    callback_text = update.message.text
    paginator = user_data["shop_paginator"]
    
    paginator.do_action(callback_text)

    text, reply_markup = paginator.page_text(), paginator.show_page()
    
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )
    
    return SHOP


async def show_shop_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # показать айтем в чате с кнопками для взаимодействия
    pass


async def show_basket(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # клавиатура через ItemPaginator со списком всех книг в корзине
    # при нажатии появляется соответствующее описание книги в чате с кнопками
    pass


async def show_inventory(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    # две кнопки: "книги в обработке" и "нужно отдать"
    # первая для книг, которые ещё не успел получить
    # вторая для книг, которые нужно будет отдать
    pass


async def show_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",  
        reply_markup=ReplyGenerator.profile_markup()
    )
    
    return PROFILE


async def change_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    student = ctx.user_data["student"]
    
    await update.message.reply_text(
        text=f"Введите новый логин. Требования:\n\n1. Логин должен быть уникальным.\n2. Буквы латинского алфавита, цифры и нижнее подчёркивание.\n3. От 2 до 32 символов.\n\nТекущий логин: {student.login}."
    )
    
    return CHANGE_LOGIN


async def changing_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    student = user_data["student"]
    login = update.message.text
    
    if check_login(login=login):
        change_db_login(student_id=student.id, new_login=login)
        
        student = get_student(login=login)
        user_data["student"] = student
        
        await update.message.reply_text(
            text=f"Успешно! Ваш логин - {login}.",
            reply_markup=ReplyGenerator.profile_markup()
        )
        
        return PROFILE
    else:
        await update.message.reply_text(
            text="Логин не соответствует требованиям. Попробуйте ещё раз."
        )
        
        return CHANGE_LOGIN


async def change_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Введите новый пароль. Требования:\n\n1. Буквы латинского алфавита и цифры.\n2. От 2 до 32 символов."
    )
    
    return CHANGE_PASSWORD


async def changing_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    student = user_data["student"]
    login = student.login
    password = update.message.text
    
    if check_password(password=password):
        change_db_password(student_id=student.id, new_password=password)
        
        student = get_student(login=login)
        user_data["student"] = student

        await update.message.reply_text(
            text=f"Успешно!",
            reply_markup=ReplyGenerator.profile_markup()
        )
        
        return PROFILE
    else:
        await update.message.reply_text(
            text="Пароль не соответствует требованиям. Попробуйте ещё раз."
        )
        
        return CHANGE_PASSWORD


async def show_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",
        reply_markup=ReplyGenerator.menu_markup()
    )
    
    return MENU


async def quit_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    pass


#! сделать выход по желанию из ввода логина и пароля (добавить клавиатуру с кнопкой "Выход")