import datetime
import logging
import os
from logging.config import fileConfig
from pathlib import Path
from typing import Dict

import requests
from dotenv import load_dotenv
from pymongo import MongoClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class DataCollector:
    URL: str = 'https://opendata.concordia.ca/API/v1/library/occupancy/'

    def run(self):
        data = self.collect()
        self.save(data)

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
        return data

    def save(self, data):
        connection = MongoClient(f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@mongo-db:27017/")
        db = connection[os.getenv('MONGO_INITDB_DATABASE')]

        for key in data:
            collection = db.key
            collection.insert_one(data.get(key))
            logger.debug(f"Inserted data for {key} with {data.get(key)}")


if __name__ == '__main__':
    data_collector = DataCollector()
    data_collector.run()
