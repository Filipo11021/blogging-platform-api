from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DB_URL = os.getenv('DB_URL', "sqlite:///./sql_app.db")
database_name = SQLALCHEMY_DB_URL.split(':')[0]
engine = None

if database_name == 'sqlite':
    engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()