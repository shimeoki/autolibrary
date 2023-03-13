from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.constants import PROFILE, CHANGE_LOGIN, CHANGE_PASSWORD
from bot.utils.markups import profile_markup, changing_credentials_markup
from bot.utils.change_credentials import check_login, check_password, change_student_login, change_student_password
from bot.utils.db_methods import get_student


async def show_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Выберите дальнейшее действие",  
        reply_markup=profile_markup()
    )
    
    return PROFILE


async def change_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    student = ctx.user_data["student"]
    
    await update.message.reply_text(
        text=f"Введите новый логин. Требования:\n\n1. Логин должен быть уникальным.\n2. Буквы латинского алфавита, цифры и нижнее подчёркивание.\n3. От 2 до 32 символов.\n\nТекущий логин: {student.login}.",
        reply_markup=changing_credentials_markup()
    )
    
    return CHANGE_LOGIN


async def changing_login(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    student = user_data["student"]
    login = update.message.text
    
    if check_login(login=login):
        change_student_login(student_id=student.id, new_login=login)
        
        student = get_student(login=login)
        user_data["student"] = student
        
        await update.message.reply_text(
            text=f"Успешно! Ваш логин - {login}.",
            reply_markup=profile_markup()
        )
        
        return PROFILE
    else:
        await update.message.reply_text(
            text="Логин не соответствует требованиям. Попробуйте ещё раз.",
            reply_markup=changing_credentials_markup()
        )
        
        return CHANGE_LOGIN


async def change_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        text="Введите новый пароль. Требования:\n\n1. Буквы латинского алфавита и цифры.\n2. От 2 до 32 символов.",
        reply_markup=changing_credentials_markup()
    )
    
    return CHANGE_PASSWORD


async def changing_password(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = ctx.user_data
    student = user_data["student"]
    login = student.login
    password = update.message.text
    
    if check_password(password=password):
        change_student_password(student_id=student.id, new_password=password)
        
        student = get_student(login=login)
        user_data["student"] = student

        await update.message.reply_text(
            text=f"Успешно!",
            reply_markup=profile_markup()
        )
        
        return PROFILE
    else:
        await update.message.reply_text(
            text="Пароль не соответствует требованиям. Попробуйте ещё раз.",
            reply_markup=changing_credentials_markup()
        )
        
        return CHANGE_PASSWORD
    

async def quit_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data.clear()
    
    await update.message.reply_text(
        text="До встречи!"
    )
    
    return ConversationHandler.END