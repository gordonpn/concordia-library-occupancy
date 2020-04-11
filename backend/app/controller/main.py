from flask_restful import Resource


class Main(Resource):
    def get(self):
        return {
                   "message": "You've reached the base url of this api"
               }, 200
