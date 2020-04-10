import datetime
import json
import logging
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from typing import Dict

import pytz
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)
logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class DataMigrator:

    def __init__(self):
        self.json_file = "data.json"

    def run(self):
        data = self.open_file
        self.migrate(data)

    def open_file(self) -> Dict[str, Dict[str, int]]:
        if not os.path.exists(self.json_file):
            sys.exit(1)

        logger.debug(f"Opening existing {self.json_file}")
        with open(self.json_file, "r") as read_file:
            data_from_json: Dict[str, Dict[str, int]] = json.load(read_file)

        logger.debug("Read file successfully")
        return data_from_json

    def migrate(self, data):
        logger.debug("Starting data migration")
        logger.debug("Making connection to mongodb")
        dbname: str = os.getenv('MONGO_INITDB_DATABASE')
        username: str = os.getenv('MONGO_NON_ROOT_USERNAME')
        password: str = os.getenv('MONGO_NON_ROOT_PASSWORD')
        uri: str = f"mongodb://{username}:{password}@mongo-db:27017/{dbname}"
        connection = MongoClient(uri)
        db = connection[dbname]
        logger.debug(f"Connection with mongodb db: {dbname}")

        for key, value in data.items():
            date_time = key.split('_')
            date = date_time[0].split('-')
            time = date_time[1].split(':')
            year = date[0]
            month = date[1]
            day = date[2]
            hour = time[0]
            minute = time[1]
            timezone = pytz.timezone('America/Montreal')
            aware_datetime = timezone.localize(
                datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            )

            for lib, occupancy in value.items():
                collection = db[lib]
                logger.debug(f"Inserting data into collection {collection}")
                collection.insert_one({
                    "time": aware_datetime,
                    "occupancy": occupancy
                })
                logger.debug(f"Inserted data for {lib} with {occupancy} occupancy at {aware_datetime}")
                logger.debug(f"Into {db}")


if __name__ == "__main__":
    data_migration = DataMigrator()
    data_migration.run()
