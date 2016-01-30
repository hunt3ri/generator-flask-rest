import json
import os

from flask import Flask, make_response
from flask_restful import Api
from mongoengine import connect, Document
from pymongo import uri_parser


def bootstrap_app():
    """
    Bootstrap function that intialises the app and config
    """
    app = Flask(__name__)

    # Load Config, default to Dev if config environment var not set
    env = os.environ.get('FLASK_REST_CONFIG', 'Dev')
    app.config.from_object('app.config.%sConfig' % env.capitalize())

    # Initialise mongo db with app instance and config
    if 'MONGODB_SETTINGS' in app.config:
        # Connection settings provided as a dictionary.
        create_mongo_connection(app.config['MONGODB_SETTINGS'])
    else:
        # Connection settings provided in standard format.
        settings = {'alias': app.config.get('MONGODB_ALIAS', None),
                    'db': app.config.get('MONGODB_DB', None),
                    'host': app.config.get('MONGODB_HOST', None),
                    'password': app.config.get('MONGODB_PASSWORD', None),
                    'port': app.config.get('MONGODB_PORT', None),
                    'username': app.config.get('MONGODB_USERNAME', None)}
        create_mongo_connection(settings)

    define_flask_restful_routes(app)

    # Register web blueprint to allow us to show welcome page
    from .web import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def define_flask_restful_routes(app):
    """
    Define the routes the API we expose using Flask-Restful see docs here
    http://flask-restful-cn.readthedocs.org/en/0.3.5/quickstart.html#endpoints
    :param app: The flask app we're initialsing
    """
    # Import API classes
    from app.api.resolutions import Resolutions
    from app.api.swagger_docs import SwaggerDocs

    api = Api(app, default_mediatype='application/json')

    # Setup API routes
    api.add_resource(Resolutions, '/api/resolution', endpoint="post_resolution", methods=['POST'])
    api.add_resource(Resolutions, '/api/resolution/<string:res_id>', endpoint="resolution", methods=['GET', 'PUT', 'DELETE'])
    api.add_resource(SwaggerDocs, '/api/docs')


def output_json(obj, status_code, headers=None):
    """
    Use customised JSON formatter because Mongo objects get serilaized to json twice otherwise.
    :param obj: The object to serialize as JSON
    :param status_code: The HTTP status code that will be returned with the response
    :param headers: Any HTTP headers that should be returned
    :return: HTTP response containing the JSON, Status Code and Headers
    """

    # If the object is a Mongo Document make sure we use the inbuilt serializer to avoid corrupted output.
    if isinstance(obj, Document):
        json_output = obj.to_json()
    else:
        try:
            json_output = json.dumps(obj)
        except TypeError:
            raise TypeError("Object is not JSON serializable, try passing dict representation instead, eg obj.__dict__")

    resp = make_response(json_output, status_code)
    resp.headers.extend(headers or {})

    return resp


def create_mongo_connection(conn_settings):
    """
    Parse connection settings and initialise connection to Mongo Database.  Method from flask_mongoengine project,
    with many thanks - https://github.com/MongoEngine/flask-mongoengine
    :param conn_settings: Settings read from config file
    """

    # Handle multiple connections recursively
    if isinstance(conn_settings, list):
        connections = {}
        for conn in conn_settings:
            connections[conn.get('alias')] = create_mongo_connection(conn)
        return connections

    # Ugly dict comprehension in order to support python 2.6
    conn = dict((k.lower(), v) for k, v in conn_settings.items() if v is not None)

    if 'replicaset' in conn:
        conn['replicaSet'] = conn.pop('replicaset')

    # Handle uri style connections
    if "://" in conn.get('host', ''):
        uri_dict = uri_parser.parse_uri(conn['host'])
        conn['db'] = uri_dict['database']

    # Connect to mongo :-)
    connect(conn.pop('db', 'test'), **conn)
