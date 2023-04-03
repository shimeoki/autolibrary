from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import LOGIN, PASSWORD, MENU
from bot.utils.paginator import Paginator
from bot.utils.markups import menu_markup
from bot.utils.db_methods import get_student
from db.password import verify_password


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    user_data["student"] = None
    
    user_data["total_price"] = 0
    user_data["basket_list"] = []
    
    user_data["inventory_filter"] = None
    
    user_data["shop_paginator"] = Paginator(rows=3, columns=2, additional_button="Фильтры")
    user_data["basket_paginator"] = Paginator(rows=3, columns=2, additional_button="Оформить заказ", book_list=[])
    user_data["inventory_paginator"] = Paginator(rows=3, columns=2, additional_button="В инвентарь", book_list=[])
    
    user_data["shop_filters"] = {"title": None, "author": None}
    
    
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
        reply_markup=menu_markup()
    )
    
    return MENU