from flask_restful import Resource
from app.models.resolution import Resolution

class Resolutions(Resource):

    def get(self):
        resolution = Resolution()
        resolution.title = "Iain"

        resolution.save()

        return {'hello': 'world'}