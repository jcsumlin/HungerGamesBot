import os
import sys

import sqlalchemy as db
from loguru import logger


if not os.path.isfile("../config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    engine = db.create_engine(f'postgresql://{config.POSTGRESS_USER}:{config.POSTGRESS_PASS}@{config.POSTGRESS_HOST}/{config.POSTGRESS_DB}')

    def __init__(self):
        self.connection = self.engine.connect()
        logger.debug("DB Instance created")


