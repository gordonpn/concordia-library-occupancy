import requests
import datetime
import json
import logging
import os
import random
import time
from logging.config import fileConfig
from pathlib import Path
from typing import Dict
from pymongo import MongoClient

from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class DataCollector:
    PATH: str = 'data.json'
    URL: str = 'https://opendata.concordia.ca/API/v1/library/occupancy/'

    def run(self):
        time.sleep(self.random_delay())
        data = self.collect()
        self.save(data)

    def random_delay(self) -> int:
        random_time: int = random.randint(0, 30) * 60
        logger.debug(f"Wait time unless next: {random_time} seconds")
        return random_time

    def collect(self) -> Dict[str, int]:
        data: Dict[str, int] = {}
        request_json: Dict[str, Dict[str, str]] = requests.get(
            DataCollector.URL,
            auth=(os.getenv('OPEN_DATA_USER'), os.getenv('OPEN_DATA_KEY'))).json()
        logger.debug(f"Collected data")
        data['Webster'] = max(0, int(float(request_json.get('Webster').get('Occupancy'))))
        data['Vanier'] = max(0, int(float(request_json.get('Vanier').get('Occupancy'))))
        data['GreyNuns'] = max(0, int(float(request_json.get('GreyNuns').get('Occupancy'))))
        return data

    def save(self, data):
        date_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
        connection = MongoClient(f"mongodb://{os.getenv('MONGO_INITDB_USERNAME')}:{os.getenv('MONGO_INITDB_PASSWORD')}@localhost:27017/")
        db = connection[os.getenv('MONGO_INITDB_DATABASE')]
        # TODO insert documents
        if os.path.exists(DataCollector.PATH):
            try:
                logger.info("Opening existing json")
                with open(DataCollector.PATH, "r") as read_file:
                    data_from_json = json.load(read_file)
            except ValueError:
                logger.error("File was empty, creating new data")
                data: Dict[str, float] = {}

            data_from_json[date_time] = data
        else:
            data_from_json = {date_time: data}

        logger.info("Writing new data into the json")
        with open(DataCollector.PATH, "w+") as write_file:
            json.dump(data_from_json, write_file, indent=4)


if __name__ == '__main__':
    data_collector = DataCollector()
    data_collector.run()
