from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.orm import sessionmaker

filename = "test.db"
engine = create_engine('sqlite:///'+filename, echo=True)
Base = declarative_base()
Meta = Base.metadata


def use_db():
    sessionm = sessionmaker(bind=engine)
    sessionm.configure(bind=engine)  # once engine is available
    session = sessionm()
    logging.info("Use Db Completed")
    return session

