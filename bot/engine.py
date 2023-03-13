from sqlalchemy import create_engine

from bot.tokens import db_token

engine = create_engine(db_token)