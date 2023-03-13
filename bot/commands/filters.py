from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import FILTERS, CHANGE_FILTER
from bot.utils.markups import filters_markup


async def show_filters(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    callback_text = update.message.text
    
    if callback_text != "Фильтры":
        if not changing_filter:
            pass
        else:
            value = callback_text if callback_text != "ОТМЕНА" else None
            user_data["shop_filters"].update({user_data["changing_filter"]: value})
            user_data["changing_filter"] = None
    
    title = user_data["shop_filters"].get("title")
    if not title:
        title = "Нет фильтра"
    
    author = user_data["shop_filters"].get("author")
    if not author:
        author = "Нет фильтра"
    
    
    await update.message.reply_text(
        text="Выберите фильтр для изменения.",
        reply_markup=filters_markup(title=title, author=author)
    )

    return FILTERS


async def changing_filter(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data

    try:
        callback_text = update.message.text.split("\n")[0][:-1]
    except ValueError:
        return FILTERS
    
    if callback_text == "Название":
        changing_filter = "title"
    elif callback_text == "Автор":
        changing_filter = "author"
    else:
        changing_filter = None
    
    user_data["changing_filter"] = changing_filter
    
    await update.message.reply_text(
        text=f'Введите значение для изменения фильтра "{callback_text}". Если вы хотите очистить фильтр, введите "ОТМЕНА".'
    )

    return CHANGE_FILTER


