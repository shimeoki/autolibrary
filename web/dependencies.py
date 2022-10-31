from json import load

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


with open('D:/GitHub/.misc/tokens.json', 'r') as f:
    db_token = load(f)["db-token"]
    
engine = create_engine(db_token)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionLocal()
    try: 
        yield session
    finally:
        session.commit()
        session.close()