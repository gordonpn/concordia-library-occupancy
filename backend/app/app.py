import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from .controller.base import Base
from .controller.occupancy_library import OccupancyLibrary
from .controller.occupancy_weekday import OccupancyWeekday
from .controller.occupancy_period import OccupancyPeriod
from .database import database

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, override=True)

debug_mode: bool = str(os.getenv('DEV')).lower().__eq__('true')

app = Flask(__name__)
database.initialize_db(app)
api = Api(app)

base_url: str = '/api/v1'

api.add_resource(Base, base_url)
api.add_resource(OccupancyLibrary, f"{base_url}/occupancy/<string:library_name>")
api.add_resource(OccupancyWeekday, f"{base_url}/occupancy/<string:library_name>/<string:weekday>")
api.add_resource(OccupancyPeriod, f"{base_url}/occupancy/<string:library_name>/last/<int:number>/<string:period>")

app.run(debug=debug_mode)
