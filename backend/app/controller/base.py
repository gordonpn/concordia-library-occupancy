import datetime
import logging
from logging.config import fileConfig

from flask_restful import Resource

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)


class Base(Resource):
    def get(self):
        logger.debug(f"GET was called at {datetime.datetime.now()}")
        return {
                   "message": "You've reached the base url of this api"
               }, 200
