import datetime
import logging
import os
import time
from logging.config import fileConfig
from pathlib import Path
from typing import Dict

import requests
import schedule
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class DataCollector:
    URL: str = 'https://opendata.concordia.ca/API/v1/library/occupancy/'

    def run(self):
        schedule.every(10).to(20).minutes.do(self.job())

        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        self.save(self.collect())

    def collect(self):
        data = {}

        request_json: Dict[str, Dict[str, str]] = requests.get(
            DataCollector.URL,
            auth=(os.getenv('OPEN_DATA_USER'), os.getenv('OPEN_DATA_KEY'))).json()
        logger.debug(f"Collected data")

        recorded_time: datetime = datetime.datetime.utcnow()

        data['Webster'] = {
            "time": recorded_time,
            "occupancy": max(0, int(float(request_json.get('Webster').get('Occupancy'))))
        }
        data['Vanier'] = {
            "time": recorded_time,
            "occupancy": max(0, int(float(request_json.get('Vanier').get('Occupancy'))))
        }
        data['GreyNuns'] = {
            "time": recorded_time,
            "occupancy": max(0, int(float(request_json.get('GreyNuns').get('Occupancy'))))
        }

        logger.debug("Finished collecting data")
        return data

    def save(self, data):
        logger.debug("Making connection to mongodb")
        dbname: str = os.getenv('MONGO_INITDB_DATABASE')
        username: str = os.getenv('MONGO_NON_ROOT_USERNAME')
        password: str = os.getenv('MONGO_NON_ROOT_PASSWORD')
        uri: str = f"mongodb://{username}:{password}@mongo-db:27017/{dbname}"
        connection = MongoClient(uri)
        db = connection[dbname]

        for key in data:
            collection = db[key]
            logger.debug(f"Inserting data into collection {collection}")
            collection.insert_one(data.get(key))
            logger.debug(f"Inserted data for {key} with {data.get(key)}")
            logger.debug(f"Into {db}")


if __name__ == '__main__':
    data_collector = DataCollector()
    data_collector.run()
