from flask import Flask
from flask_restful import Api
from .api.resources.resolution import Resolution
import os


def bootstrap_app():
    """
    Bootstrap function that intialises the app and config
    """
    app = Flask(__name__)

    # Load Config, default to Dev if config environment var not set
    env = os.environ.get('FLASK_REST_CONFIG', 'Dev')
    app.config.from_object('app.config.%sConfig' % env.capitalize())

    # Initialise flask_restful with app instance
    api = Api(app)
    
    # Setup API routes
    api.add_resource(Resolution,
                     '/api/resolution',
                     '/api/resolution/<int:res_id>', endpoint='test')
                     
    # Register web blueprint to allow us to show welcome page
    from .web import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
