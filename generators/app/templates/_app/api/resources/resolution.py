from flask_restful import Resource

class Resolution(Resource):

    def get(self):
        return {'hello': 'world'}