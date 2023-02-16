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
    LOGIN,
    PASSWORD,
    MENU,
    SHOP,
    PROFILE,
    CHANGE_LOGIN,
    CHANGE_PASSWORD,
    BASKET,
    INVENTORY,
    start,
    enter_login,
    enter_password,
    show_shop,
    show_shop_item,
    show_shop_item_handler,
    show_basket,
    show_basket_item,
    show_basket_item_handler,
    show_inventory_buttons,
    show_profile,
    show_main_menu,
    change_login,
    changing_login,
    change_password,
    changing_password,
    order_checkout,
    quit_profile,
    show_inventory,
    show_inventory_item
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
        },
        fallbacks=[MessageHandler(filters.Regex("^Выход$"), quit_profile)]
    )
    
    app.add_handler(conversation_handler)
    
    app.run_polling()
    

if __name__ == "__main__":
    main()