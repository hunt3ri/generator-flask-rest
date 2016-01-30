from flask import current_app, jsonify
from flask_restful import Resource
from flask_swagger import swagger


class SwaggerDocs(Resource):

    def get(self):
        """
        Generate YAML feed suitable for Swagger UI to consume
        ---
        tags:
          - docs
        responses:
          200:
            description: Swagger YAML successfully generated
        """
        return jsonify(swagger(current_app))
