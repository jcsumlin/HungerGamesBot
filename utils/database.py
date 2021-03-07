import os
import sys

import sqlalchemy as db
from loguru import logger

from sqlalchemy import MetaData, Table, Column, String, Integer, create_engine
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

if not os.path.isfile("../config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Database:
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


class Tribute(Base):
    __tablename__ = 'tribute'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)


class ItemType(Base):
    __tablename__ = 'item_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # weapon/medicine


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(Integer)


class TributesItem(Base):
    __tablename__ = 'tributes_item'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, nullable=False)
    tribute_id = Column(Integer, nullable=False)
    item_id = Column(Integer, nullable=False)


class Alliance(Base):
    __tablename__ = 'alliance'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, nullable=False)
    tribute_1 = Column(Integer, nullable=False)
    tribute_2 = Column(Integer, nullable=False)


class HungerGame(Base):
    __tablename__ = "hunger_game"
    id = Column(Integer, primary_key=True)
    title = Column(String, default="Hunger Games", nullable=False)
    game_master = Column(Integer, nullable=False)  # User.id
    winner = Column(Integer, nullable=True)  # User.id
    winner_tribute = Column(String, nullable=True)  # Tribute of winner


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    data = Column(JSONB, nullable=False)  # JSON blob containing event information


if __name__ == "__main__":
    path = f'postgresql://{config.POSTGRESS_USER}:{config.POSTGRESS_PASS}@{config.POSTGRESS_HOST}/{config.POSTGRESS_DB}'
    engine = create_engine(path, echo=True)
    Base.metadata.create_all(engine)
