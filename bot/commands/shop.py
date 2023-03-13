from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.constants import SHOP, INVENTORY
from bot.utils.db_methods import get_book, get_book_by_id


async def show_shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    callback_text = update.message.text
    paginator = user_data["shop_paginator"]
    
    title = user_data["shop_filters"].get("title")
    author = user_data["shop_filters"].get("author")
    
    paginator.update_books(title=title, author=author)
    
    if callback_text in ["<", ">"]:
        paginator.do_action(callback_text)
    else:
        paginator.current_page = 1

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