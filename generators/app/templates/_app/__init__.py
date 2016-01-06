from flask import Flask
from flask_restful import Api
from .api.resources.resolution import Resolution
import os


def bootstrap_app():
    """
    Bootstrap function that intialises the app and any config
    """
    app = Flask(__name__)

    # Set Config, default to Dev if config not set
    env = os.environ.get('FLASK_REST_CONFIG', 'Dev')
    app.config.from_object('app.config.%sConfig' % env.capitalize())

    # Initialise flask_restful with app instance
    api = Api(app)
    
    # Setup API routes
    api.add_resource(Resolution,
                     '/api/resolution',
                     '/api/resolution/<int:res_id>', endpoint='test')
    
    return app
