import logging
from json import load

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from commands import (
    START,
    LOGIN,
    PASSWORD, 
    start,
    login,
    password
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

with open('tokens.json', 'r') as f:
    bot_token = load(f)["bot-token"]


def main() -> None:
    app = Application.builder().token(bot_token).build()
    
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START: [
                MessageHandler(filters.Regex(filters.TEXT & ~filters.COMMAND), login)
            ],
            LOGIN: [
                MessageHandler(filters.Regex(filters.TEXT & ~filters.COMMAND), password)
            ],
            PASSWORD: [
                # MessageHandler(condition, menu)
            ],
            # MENU: [
            #     MessageHandler()
            # ]
        },
        # fallbacks=[]
    )
    
    app.add_handler(conversation_handler)
    
    app.run_polling()

    
if __name__ == "__main__":
    main()