import logging

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters
)

from bot.commands.authorization import enter_login, enter_password, start
from bot.commands.menu import show_main_menu
from bot.commands.shop import show_shop, show_shop_item, show_shop_item_handler
from bot.commands.filters import show_filters, changing_filter
from bot.commands.inventory import show_inventory, show_inventory_buttons, show_inventory_item
from bot.commands.basket import show_basket, show_basket_item, show_basket_item_handler, order_checkout
from bot.commands.profile import show_profile, quit_profile, change_login, changing_login, change_password, changing_password
from bot.constants import *

from bot.tokens import bot_token


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(bot_token).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LOGIN: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), enter_login)
            ],
            PASSWORD: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), enter_password)
            ],
            MENU: [
                MessageHandler(filters.Regex("^Магазин$"), show_shop),
                MessageHandler(filters.Regex("^Корзина$"), show_basket),
                MessageHandler(filters.Regex("^Инвентарь$"), show_inventory_buttons),
                MessageHandler(filters.Regex("^Личный кабинет$"), show_profile)
            ],
            PROFILE: [
                MessageHandler(filters.Regex("^Поменять логин$"), change_login),
                MessageHandler(filters.Regex("^Поменять пароль$"), change_password),
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu)
            ],
            CHANGE_LOGIN: [
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), changing_login)
            ],
            CHANGE_PASSWORD: [
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), changing_password)
            ],
            SHOP: [
                MessageHandler(filters.Regex("^<$"), show_shop),
                MessageHandler(filters.Regex("^>$"), show_shop),
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu),
                MessageHandler(filters.Regex("^Фильтры$"), show_filters),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), show_shop_item),
                CallbackQueryHandler(show_shop_item_handler)
            ],
            BASKET: [
                MessageHandler(filters.Regex("^<$"), show_basket),
                MessageHandler(filters.Regex("^>$"), show_basket),
                MessageHandler(filters.Regex("^Оформить заказ$"), order_checkout),
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), show_basket_item),
                CallbackQueryHandler(show_basket_item_handler)
            ],
            INVENTORY: [
                MessageHandler(filters.Regex("^(В обработке|Для выдачи|На руках)$"), show_inventory),
                MessageHandler(filters.Regex("^<$"), show_inventory),
                MessageHandler(filters.Regex("^>$"), show_inventory),
                MessageHandler(filters.Regex("^Обратно в инвентарь$"), show_inventory_buttons),
                MessageHandler(filters.Regex("^Обратно в меню$"), show_main_menu),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), show_inventory_item)
            ],
            FILTERS: [
                MessageHandler(filters.Regex("^Обратно в магазин$"), show_shop),
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), changing_filter)
            ],
            CHANGE_FILTER: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Выход$")), show_filters)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Выход$"), quit_profile)]
    )
    
    app.add_handler(conversation_handler)
    
    app.run_polling()
    

if __name__ == "__main__":
    main()