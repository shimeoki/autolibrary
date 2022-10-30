from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from json import load
from uvicorn import run

from db import crud, models, schemas


with open('D:/GitHub/.misc/tokens.json', 'r') as f:
    db_token = load(f)["db-token"]
    
engine = create_engine(db_token)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    session = SessionLocal()
    try: 
        yield session
    finally:
        session.commit()
        session.close()
        

@app.post("/book_genres/", response_model=schemas.BookGenre)
def create_book_genre(book_genre: schemas.BookGenreCreate, session: Session = Depends(get_db)):
    methods = crud.BookGenreRepo(session=session)
    
    db_book_genre = methods.create(book_genre=book_genre)
    
    return db_book_genre

if __name__ == '__main__':
    run('web.main:app', reload=True, log_level="info")