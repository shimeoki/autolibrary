from json import load

from telegram import Update
from telegram.ext import ContextTypes

from sqlalchemy import create_engine

from ..db.models import (
    Students
)

from utils import (
    ItemGetter
)


with open('D:\GitHub\.misc\tokens.json', 'r') as f:
    db_token = load(f)["db-token"]
    
engine = create_engine(db_token)

START, LOGIN, PASSWORD, MENU = range(4)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    
    user_data["login"] = None
    user_data["login_status"] = None
    user_data["first_name"] = None
    user_data["last_name"] = None
    user_data["current_books"] = []
    user_data["current_order"] = []
    
    text = "Привет! Введи свой логин, чтобы продолжить."
    
    await update.message.reply_text(
        text=text
    )
    
    return START


async def login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    login = update.message.text
    
    getter = ItemGetter(engine, Students)
    student = getter.get_item("login", login)
    
    if not student:
        text = "Логин неверный, попробуйте ещё раз."
        
        await update.message.reply_text(
            text=text
        )

        return START

    user_data["login"] = login

    text = "Введите пароль."
    
    await update.message.reply_text(
        text=text
    )
    
    return LOGIN


async def password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    password = update.message.text
    
    getter = ItemGetter(engine, Students)
    student = getter.get_item("login", user_data["login"])
    
    if student.password != password:
        text = "Пароль неверный, попробуйте ещё раз."
        
        await update.message.reply_text(
            text=text
        )

        return LOGIN

    user_data["login_status"] = True
    user_data["first_name"] = student.first_name
    user_data["last_name"] = student.last_name
    
    text = "Успешный вход!"
    
    await update.message.reply_text(
        text=text
        #тут должнен быть reply markup menu
    )
    
    return MENU