import logging
from os import unlink, path

from sqlalchemy.orm import sessionmaker

from db import filename, engine, Base




def init_db():
    if path.isfile(filename):
        unlink(filename)
    # Create db now
    Base.metadata.create_all(engine)
    smsession = sessionmaker(bind=engine)
    smsession.configure(bind=engine)  # once engine is available
    session = smsession()
    return session

