import os
import sys

import sqlalchemy as db
from loguru import logger

from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

if not os.path.isfile("../config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine(
        f'postgresql://{config.POSTGRESS_USER}:{config.POSTGRESS_PASS}@{config.POSTGRESS_HOST}/{config.POSTGRESS_DB}')

    def __init__(self):
        connection = self.engine.connect()
        self.session = Session(bind=connection)

        logger.debug("DB Instance created")


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    wins = Column(Integer)

    def __repr__(self):
        return "<User(id='%s', wins='%s')>" % (self.id, self.wins)


class HungerGame(Base):
    __tablename__ = "hunger_game"
    id = Column(Integer, primary_key=True)
    title = Column(String, default="Hunger Games", nullable=False)
    created_by = Column(Integer, nullable=False)  # User.id
    winner = Column(Integer, nullable=True)  # User.id



if __name__ == "__main__":
    path = f'postgresql://{config.POSTGRESS_USER}:{config.POSTGRESS_PASS}@{config.POSTGRESS_HOST}/{config.POSTGRESS_DB}'
    engine = create_engine(path, echo=True)
    Base.metadata.create_all(engine)
