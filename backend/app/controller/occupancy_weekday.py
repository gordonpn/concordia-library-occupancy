from flask_restful import Resource


class OccupancyWeekday(Resource):
    def get(self, library_name: str, weekday: str):
        # TODO return all data based on param
        pass
