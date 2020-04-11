import logging
import os
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from flask_pymongo import PyMongo

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

mongo = PyMongo()


def initialize_db(app):
    logger.debug("Making connection to mongodb")
    dbname: str = os.getenv('MONGO_INITDB_DATABASE')
    username: str = os.getenv('MONGO_NON_ROOT_USERNAME')
    password: str = os.getenv('MONGO_NON_ROOT_PASSWORD')
    uri: str = f"mongodb://{username}:{password}@mongo-db:27017/{dbname}"
    mongo.init_app(app=app, uri=uri)
