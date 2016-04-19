import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from logging.handlers import RotatingFileHandler
from migrations.dynamo import migration_runner


app = Flask(__name__)


def bootstrap_app():
    """
    Bootstrap function that intialises the app and config
    """
    # Load Config, default to Dev if config environment var not set
    env = os.environ.get('FLASK_MICRO_CONFIG', 'Dev')
    app.config.from_object('app.config.%sConfig' % env.capitalize())

    initialise_logger()
    app.logger.info('AWS-Flask-Micro Starting Up')

    run_dynamo_migrations(env)

    define_api_routes()
    app.logger.info('API Routes defined')

    # Register web blueprint to allow us to show welcome page
    from .web import main as main_blueprint
    from .web import swagger as swagger_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(swagger_blueprint)

    # Allow CORS on all requests
    app.logger.info('Allowing CORS on all requests')
    CORS(app)

    return app


def initialise_logger():
    """
    Read environment config then initialise a 1MB rotating log.  Prod Log Level can be reduced to help diagnose Prod
    only issues.
    """

    log_dir = app.config['LOG_DIR']
    log_level = app.config['LOG_LEVEL']

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(log_dir + '/map-store-api.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    app.logger.addHandler(file_handler)
    app.logger.setLevel(log_level)


def run_dynamo_migrations(environment):
    """
    Create any necessary Dynamo tables for the current environment
    :param environment: The current running environment, eg Dev, Staging etc
    """
    app.logger.info('Running DynamoDB Migrations')
    migration_runner.run(environment, app.logger, app.config['DYNAMODB_CONFIG'])


def define_api_routes():
    """
    Define the routes the API we expose using Flask-Restful see docs here
    http://flask-restful-cn.readthedocs.org/en/0.3.5/quickstart.html#endpoints
    """
    # Import API classes
    from app.api.resolutions import Resolutions
    from app.api.swagger_docs import SwaggerDocs

    api = Api(app, default_mediatype='application/json')

    # Setup API routes
    api.add_resource(Resolutions, '/api/resolution', endpoint="post_resolution", methods=['POST'])
    api.add_resource(Resolutions, '/api/resolution/<string:res_id>', endpoint="resolution", methods=['GET', 'PUT', 'DELETE'])
    api.add_resource(SwaggerDocs, '/api/docs')
