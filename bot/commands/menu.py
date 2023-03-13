from telegram import Update
from telegram.ext import ContextTypes

from bot.constants import MENU
from bot.utils.markups import menu_markup


async def show_main_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",
        reply_markup=menu_markup()
    )
    
    return MENU