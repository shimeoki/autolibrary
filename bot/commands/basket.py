from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from bot.constants import BASKET, INVENTORY, MENU
from bot.utils.db_methods import get_book, get_book_by_id, reserve_book
from bot.utils.markups import menu_markup


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
            reply_markup=menu_markup()
        )

        return MENU
    
    count = 0
    
    for book in user_data["basket_list"]:
        result = reserve_book(student_id=user_data["student"].id, book_id=book.id)
        
        if not result:
            for j in range(count):
                user_data["basket_list"].pop(0)
            
            await update.message.reply_text(
                text="Произошла непредвиденная ошибка. Книги, которые были заказаны, удалены из вашей корзины.",
                reply_markup=menu_markup()
            )
            
            return MENU
        
        count += 1
        
    user_data["basket_list"].clear()
    
    await update.message.reply_text(
        text="Книги успешно заказаны.",
        reply_markup=menu_markup()
    )

    return MENU