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
        swag = swagger(current_app)
        swag['info']['title'] = "Flask-Rest"
        swag['info']['description'] = "Flask-Rest turbocharged Rest/MicroService Development"
        swag['info']['version'] = "0.1.0"

        return jsonify(swag)
