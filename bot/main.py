from email.message import Message
import logging
from json import load

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from bot.commands import (
    START,
    LOGIN,
    PASSWORD,
    SHOP,
    start,
    enter_login,
    enter_password,
    show_shop,
    show_shop_item,
    show_basket,
    show_inventory,
    show_profile,
    show_main_menu,
    quit_profile
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

with open('D:/GitHub/.misc/tokens.json', 'r') as f:
    bot_token = load(f)["bot-token"]


def main() -> None:
    app = Application.builder().token(bot_token).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), enter_login)
            ],
            LOGIN: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), enter_password)
            ],
            PASSWORD: [
                MessageHandler(filters.Regex("^Сделать заказ$"), show_shop),
                MessageHandler(filters.Regex("^Корзина$"), show_basket),
                MessageHandler(filters.Regex("^Активные книги$"), show_inventory),
                MessageHandler(filters.Regex("^Личный кабинет$"), show_profile)
            ],
            SHOP: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), show_shop_item),
                MessageHandler(filters.Regex("^<$"), show_shop),
                MessageHandler(filters.Regex("^>$"), show_shop),
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu)#,
                #CallbackQueryHandler()
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Выход$"), quit_profile)]
    )
    
    app.add_handler(conversation_handler)
    
    app.run_polling()
    

if __name__ == "__main__":
    main()