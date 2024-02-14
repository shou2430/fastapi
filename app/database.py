from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_URL = "postgresql://postgres:jason248@localhost/fastapi"

engine = create_engine(SQL_ALCHEMY_URL)

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# create independent database session for each request


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()