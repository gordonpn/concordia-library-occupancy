from flask_restful import Resource


class OccupancyPeriod(Resource):
    def get(self, library_name: str, number: int, period: str):
        # TODO return all data based on param and period
        pass
