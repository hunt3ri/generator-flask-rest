from flask_restful import Resource, reqparse, fields, marshal
from app.stores import resolution_store
from flask import request
import json



class Hello:
    def __init__(self, title):
        self.id = 1
        self.title = title

task_fields = {
    'resId': fields.String(attribute='res_id'),
    'title': fields.String,
    'url': fields.Url('resolution_route', absolute=True)
}


class Resolutions(Resource):

    def __init__(self):
        # Define request parser to validate all fields expected are present
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No title provided', location='json')
        super().__init__()

    def get(self, res_id):
        """
        Get a resolution for the supplied res_id
        ---
        tags:
          - resolutions
        responses:
          200:
            description: User Found
          404:
            description: User Not Found
          500:
            description: Server Error
        """

        resolution = resolution_store.get_or_404(res_id)

        return marshal(resolution._asdict(), task_fields), 200

    def post(self):
        """
        Create a new resolution
        ---
        tags:
          - resolutions
        responses:
          201:
            description: Resolution created
          404:
            description: User Not Found
          500:
            description: Server Error
        """

        # Get json from request as a string which mongoengine can process
        request_json = json.dumps(request.get_json())

        resolution = resolution_store.save(request_json)

        return marshal(resolution._asdict(), task_fields), 201

    # def put(self, _id):
    #
    #     try:
    #         resolution = Resolution.objects.get(id=_id)
    #     except (MultipleObjectsReturned, DoesNotExist, ValidationError):
    #         abort(404)
    #
    #     args = self.reqparse.parse_args()
    #
    #     resolution.modify(title=args['title'])
    #
    #     # Use to_mongo() method to create dict representation of object so it's compatible with flask-restful
    #     return marshal(resolution.to_mongo(), task_fields), 200
    #
    # def delete(self, _id):
    #
    #     try:
    #         resolution = Resolution.objects.get(id=_id)
    #     except (MultipleObjectsReturned, DoesNotExist, ValidationError):
    #         abort(404)
    #
    #     resolution.delete()
    #
    #     return 200