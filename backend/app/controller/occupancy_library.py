from flask_restful import Resource

from ..database.database import mongo


class OccupancyLibrary(Resource):

    def get(self, library_name: str):
        return mongo.db[library_name].find()
