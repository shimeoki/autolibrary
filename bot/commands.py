from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from bot.utils import (
    ReplyGenerator,
    BookPaginator,
    change_db_login,
    change_db_password,
    check_login,
    check_password,
    get_student,
    get_book,
    get_book_by_id,
    update_book,
    get_inventory_books
)

from db.password import verify_password

LOGIN, PASSWORD, MENU, SHOP, PROFILE, CHANGE_LOGIN, CHANGE_PASSWORD, BASKET, INVENTORY = range(9)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    user_data["student"] = None
    
    user_data["total_price"] = 0
    user_data["basket_list"] = []
    
    user_data["inventory_filter"] = None
    
    user_data["shop_paginator"] = BookPaginator(lines=3, columns=2, additional_button="Фильтры")
    user_data["basket_paginator"] = BookPaginator(lines=3, columns=2, additional_button="Оформить заказ", book_list=[])
    user_data["inventory_paginator"] = BookPaginator(lines=3, columns=2, additional_button="Обратно в инвентарь", book_list=[])
    
    
    await update.message.reply_text(
        text="Введите свой логин, чтобы продолжить."
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
    
    paginator.update_books()
    
    if callback_text in ["<", ">"]:
        paginator.do_action(callback_text)

    text, reply_markup = paginator.page_text(), paginator.show_page()
    
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )
    
    return SHOP


async def show_shop_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    callback_text = update.message.text
    
    try:
        title, author = callback_text.split("\n")
    except ValueError:
        return INVENTORY

    book = get_book(title=title, author=author)
    
    if not book:
        return SHOP

    await update.message.reply_text(
        text=f"{book.title}\n{book.author}\nЦена: {book.price}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Добавить в корзину", callback_data=book.id)]])
    )
    
    return SHOP


async def show_shop_item_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = ctx.user_data
    query = update.callback_query
    
    book = get_book_by_id(book_id=query.data)
    
    for i in user_data["basket_list"]:
        if i.id == book.id:
            await query.answer()
            await query.edit_message_text(
                text="Книга уже в вашей корзине."
            )
            
            return
    
    user_data["basket_list"].append(book)
    if book.price:
        user_data["total_price"] += book.price
    
    await query.answer()
    await query.edit_message_text(
        text="Успешно добавлено в заказ."
    )


async def show_basket(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    callback_text = update.message.text
    paginator = user_data["basket_paginator"]
    
    paginator.update_book_list(user_data["basket_list"])
    
    if callback_text in ["<", ">"]:
        paginator.do_action(callback_text)

    text, reply_markup = paginator.page_text(), paginator.show_page()
    
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

    return BASKET


async def show_basket_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    callback_text = update.message.text
    
    try:
        title, author = callback_text.split("\n")
    except ValueError:
        return INVENTORY

    book = get_book(title=title, author=author)
    
    if not book:
        return BASKET

    await update.message.reply_text(
        text=f"{book.title}\n{book.author}\nЦена: {book.price}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Удалить из корзины", callback_data=book.id)]])
    )
    
    return BASKET


async def show_basket_item_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user_data = ctx.user_data
    query = update.callback_query
    
    book = get_book_by_id(book_id=query.data)
    
    for i in user_data["basket_list"]:
        if i.id == book.id:
            user_data["basket_list"].remove(i)
            if book.price:
                user_data["total_price"] -= book.price
            
            await query.answer()
            await query.edit_message_text(
                text="Успешно удалено из заказа."
            )

            return
    
    await query.answer()
    await query.edit_message_text(
        text="Книга отсутствует в вашей корзине."
    )


async def order_checkout(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    if len(user_data["basket_list"]) == 0:
        await update.message.reply_text(
            text="Корзина пуста.",
            reply_markup=ReplyGenerator.menu_markup()
        )

        return MENU
    
    count = 0
    
    for book in user_data["basket_list"]:
        result = update_book(student_id=user_data["student"].id, book_id=book.id)
        
        if not result:
            for j in range(count):
                user_data["basket_list"].pop(0)
            
            await update.message.reply_text(
                text="Произошла непредвиденная ошибка. Книги, которые были заказаны, удалены из вашей корзины.",
                reply_markup=ReplyGenerator.menu_markup()
            )
            
            return MENU
        
        count += 1
        
    user_data["basket_list"].clear()
    
    await update.message.reply_text(
        text="Книги успешно заказаны.",
        reply_markup=ReplyGenerator.menu_markup()
    )

    return MENU
    
    
async def show_inventory_buttons(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите категорию для просмотра.",
        reply_markup=ReplyGenerator.inventory_markup()
    )

    return INVENTORY


async def show_inventory(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    callback_text = update.message.text
    
    if callback_text in ["В обработке", "Для выдачи", "На руках"]:
        user_data["inventory_filter"] = callback_text
    
    paginator = user_data["inventory_paginator"]
    book_list = get_inventory_books(
        student_id=user_data["student"].id, 
        state_name=user_data["inventory_filter"]
    )
    
    paginator.update_book_list(book_list=book_list)
    
    if callback_text in ["<", ">"]:
        paginator.do_action(callback_text)

    text, reply_markup = paginator.page_text(), paginator.show_page()
    
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

    return INVENTORY


async def show_inventory_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    callback_text = update.message.text
    
    try:
        title, author = callback_text.split("\n")
    except ValueError:
        return INVENTORY

    book = get_book(title=title, author=author)
    
    if not book:
        return INVENTORY

    await update.message.reply_text(
        text=f"{book.title}\n{book.author}\nЦена: {book.price}"
    )
    
    return INVENTORY


async def show_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",  
        reply_markup=ReplyGenerator.profile_markup()
    )
    
    return PROFILE


async def change_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    student = ctx.user_data["student"]
    
    await update.message.reply_text(
        text=f"Введите новый логин. Требования:\n\n1. Логин должен быть уникальным.\n2. Буквы латинского алфавита, цифры и нижнее подчёркивание.\n3. От 2 до 32 символов.\n\nТекущий логин: {student.login}.",
        reply_markup=ReplyGenerator.changing_credentials_markup()
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
            text="Логин не соответствует требованиям. Попробуйте ещё раз.",
            reply_markup=ReplyGenerator.changing_credentials_markup()
        )
        
        return CHANGE_LOGIN


async def change_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Введите новый пароль. Требования:\n\n1. Буквы латинского алфавита и цифры.\n2. От 2 до 32 символов.",
        reply_markup=ReplyGenerator.changing_credentials_markup()
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
            text="Пароль не соответствует требованиям. Попробуйте ещё раз.",
            reply_markup=ReplyGenerator.changing_credentials_markup()
        )
        
        return CHANGE_PASSWORD


async def show_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",
        reply_markup=ReplyGenerator.menu_markup()
    )
    
    return MENU


async def quit_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data.clear()
    
    await update.message.reply_text(
        text="До встречи!"
    )
    
    return ConversationHandler.END