from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import INVENTORY
from bot.utils.markups import inventory_markup
from bot.utils.db_methods import get_inventory_books, get_book


async def show_inventory_buttons(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите категорию для просмотра.",
        reply_markup=inventory_markup()
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
        text=f"{book.title}\n{book.author}\nДата получения: {book.receive_date}\nДата возвращения: {book.return_date}"
    )
    
    return INVENTORY