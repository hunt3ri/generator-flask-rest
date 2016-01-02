from flask import Flask
from flask_restful import Api
from .api.resources.resolution import Resolution

def bootstrap_app():
    """
    Simple bootstrap function that intialises the app and any config
    """
    app = Flask(__name__)
    api = Api(app)
    
    # Setup routes
    api.add_resource(Resolution, '/api/resolution')
    
    return app
