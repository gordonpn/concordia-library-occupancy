from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from .controller.occupancy_time import OccupancyLibraryTime
from .controller.occupancy_library import OccupancyLibrary
from .controller.main import Main
from .controller.occupancy import Occupancy

app = Flask(__name__)
api = Api(app)

api.add_resource(Main, '/api', '/api/v1')
api.add_resource(Occupancy, '/api/v1/occupancy')
api.add_resource(OccupancyLibrary, '/api/v1/occupancy/<string:library_name>')
api.add_resource(OccupancyLibraryTime, '/api/v1/occupancy/<string:library_name>/<string:period>')

app.run(debug=True)
