from flask_restful import Resource, reqparse, fields, marshal
from app.models.resolution import Resolution
from flask import abort
from mongoengine.queryset import MultipleObjectsReturned, DoesNotExist
from mongoengine.base import ValidationError


class Hello:
    def __init__(self, title):
        self.id = 1
        self.title = title

task_fields = {
    'id': fields.String(attribute='_id'),
    'title': fields.String,
    'url': fields.Url('iain_route')
}

class Resolutions(Resource):

    def __init__(self):
        # Define request parser to validate all fields expected are present
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No title provided', location='json')
        super().__init__()

    def get(self, id):

        # TODO create get_or_404 base class
        try:
            resolution = Resolution.objects.get(id=id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

        return marshal(resolution.to_mongo(), task_fields), 200

    def post(self):
        #TODO deserialize directly from_json()

        args = self.reqparse.parse_args()
        resolution = Resolution()
        resolution.title = args['title']
        resolution.save()

        # Use to_mongo() method to create dict representation of object so it's compatible with falsk-restful
        return marshal(resolution.to_mongo(), task_fields), 201

    def put(self, id):


        try:
            resolution = Resolution.objects.get(id=id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)