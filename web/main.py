from json import load

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from fastapi import FastAPI
from uvicorn import run

from web.router import api_router
from db.models import Base


app = FastAPI()
app.include_router(api_router)


@app.on_event("startup")
def startup():
    with open('D:/GitHub/.misc/tokens.json', 'r') as f:
        db_token = load(f)["db-token"]
    
    engine = create_engine(db_token)
    Base.metadata.create_all(bind=engine)
    
    session_factory = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    
    app.state.db_engine = engine
    app.state.session_factory = session_factory


if __name__ == '__main__':
    run('web.main:app', reload=True, log_level="info")