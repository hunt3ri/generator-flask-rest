from flask_restful import Resource, reqparse, fields, marshal
from app.models.resolution import Resolution
from flask import abort, request
from mongoengine.queryset import MultipleObjectsReturned, DoesNotExist
from mongoengine.base import ValidationError
import json


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

    def get(self, _id):

        # TODO create get_or_404 base class
        try:
            resolution = Resolution.objects.get(id=_id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

        return marshal(resolution.to_mongo(), task_fields), 200

    def post(self):

        # Get json from request as a string which mongoengine can process
        request_json = json.dumps(request.get_json())

        resolution = Resolution.from_json(request_json)
        resolution.save()

        # Use to_mongo() method to create dict representation of object so it's compatible with flask-restful
        return marshal(resolution.to_mongo(), task_fields), 201

    def put(self, _id):

        try:
            resolution = Resolution.objects.get(id=_id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

        args = self.reqparse.parse_args()

        resolution.modify(title=args['title'])

        # Use to_mongo() method to create dict representation of object so it's compatible with flask-restful
        return marshal(resolution.to_mongo(), task_fields), 200

    def delete(self, _id):

        try:
            resolution = Resolution.objects.get(id=_id)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)

        resolution.delete()

        return 200