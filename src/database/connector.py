from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as sa
import os

def create_engine_instance()-> tuple:
    """
    Creates and returns a SQLAlchemy engine instance.
    """
    url = os.environ['SQLALCHEMY_DATABASE_URL']
    return create_engine(url, echo=True)

def get_session_local(engine) -> any:
    """
    Creates and returns a session factory bound to the engine.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = get_session_local()
    try:
        yield db
    finally:
        db.close()
        