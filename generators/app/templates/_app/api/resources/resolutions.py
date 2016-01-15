from flask_restful import Resource, reqparse, fields, marshal
from app.models.resolution import Resolution


class Hello:
    def __init__(self, title):
        self.hello = title

task_fields = {
    'title': fields.String
}

class Resolutions(Resource):

    def __init__(self):
        # Define request parser to validate all fields expected are present
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No title provided', location='json')
        super().__init__()

    def get(self):
        #resolution = Resolution()
        #resolution.title = "Iain"

        #resolution.save()

        #return {'hello': 'world'}

        test = Hello("linda")

        return test.__dict__, 200

    def post(self):
        args = self.reqparse.parse_args()
        resolution = Resolution()
        resolution.title = args['title']
        resolution.save()

        # TODO test fields thing to modify response, test deserializing to object direct from json not picking out args

        #return marshal(resolution, task_fields), 201
        return resolution, 201