from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config import SQLALCHEMY_DATABASE_URI
from db.schema import Base

Engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=Engine)


def init_db():
    Base.metadata.create_all(Engine)
