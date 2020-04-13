from bson.json_util import dumps
from flask_restful import Resource

from ..database.database import mongo


class OccupancyLibrary(Resource):

    def get(self, library_name: str):
        return dumps(mongo.db[library_name.lower()].find())
