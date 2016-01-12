from flask import Flask
from flask_restful import Api
from .api.resources.resolutions import Resolutions
from mongoengine import connect
from pymongo import uri_parser
import os


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
        create_connection(app.config['MONGODB_SETTINGS'])
    else:
        # Connection settings provided in standard format.
        settings = {'alias': app.config.get('MONGODB_ALIAS', None),
                    'db': app.config.get('MONGODB_DB', None),
                    'host': app.config.get('MONGODB_HOST', None),
                    'password': app.config.get('MONGODB_PASSWORD', None),
                    'port': app.config.get('MONGODB_PORT', None),
                    'username': app.config.get('MONGODB_USERNAME', None)}
        create_connection(settings)

    # Initialise flask_restful with app instance
    api = Api(app)
    
    # Setup API routes
    api.add_resource(Resolutions,
                     '/api/resolution',
                     '/api/resolution/<int:res_id>', endpoint='test')
                     
    # Register web blueprint to allow us to show welcome page
    from .web import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app


def create_connection(conn_settings):
    """
    Create Connection method from flask_mongoengine project, with many thanks
    https://github.com/MongoEngine/flask-mongoengine
    """

    # Handle multiple connections recursively
    if isinstance(conn_settings, list):
        connections = {}
        for conn in conn_settings:
            connections[conn.get('alias')] = create_connection(conn)
        return connections

    # Ugly dict comprehention in order to support python 2.6
    conn = dict((k.lower(), v) for k, v in conn_settings.items() if v is not None)

    if 'replicaset' in conn:
        conn['replicaSet'] = conn.pop('replicaset')

    # Handle uri style connections
    if "://" in conn.get('host', ''):
        uri_dict = uri_parser.parse_uri(conn['host'])
        conn['db'] = uri_dict['database']

    return connect(conn.pop('db', 'test'), **conn)