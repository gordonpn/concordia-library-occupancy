import datetime
import json
import os
import random
import time
from typing import Dict

import requests

from Configuration.config import Config
from Configuration.logger import get_logger


class DataCollector:
    PATH: str = '../data.json'
    URL: str = 'https://opendata.concordia.ca/API/v1/library/occupancy/'

    def __init__(self):
        self.config = Config()
        self.logger = get_logger()

    def run(self):
        self.config.load_config()
        time.sleep(self.random_delay())
        data = self.collect()
        self.save(data)

    def random_delay(self) -> int:
        random_time: int = random.randint(0, 30) * 60
        self.logger.debug(f"Random time: {random_time}")
        return random_time

    def collect(self) -> Dict[str, int]:
        data: Dict[str, int] = {}
        request_json: Dict[str, Dict[str, str]] = requests.get(
            DataCollector.URL,
            auth=(self.config.user, self.config.key)).json()
        self.logger.debug(f"Collected data")
        data['Webster'] = max(0, int(float(request_json.get('Webster').get('Occupancy'))))
        data['Vanier'] = max(0, int(float(request_json.get('Vanier').get('Occupancy'))))
        data['GreyNuns'] = max(0, int(float(request_json.get('GreyNuns').get('Occupancy'))))
        return data

    def save(self, data):
        date_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
        if os.path.exists(DataCollector.PATH):
            try:
                self.logger.info("Opening existing json")
                with open(DataCollector.PATH, "r") as read_file:
                    data_from_json = json.load(read_file)
            except ValueError:
                self.logger.error("File was empty, creating new data")
                data: Dict[str, float] = {}

            data_from_json[date_time] = data
        else:
            data_from_json = {date_time: data}

        self.logger.info("Writing new data into the json")
        with open(DataCollector.PATH, "w+") as write_file:
            json.dump(data_from_json, write_file, indent=4)


if __name__ == '__main__':
    data_collector = DataCollector()
    data_collector.run()
