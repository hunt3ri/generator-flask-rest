from flask import Flask

def bootstrap_app():
    """
    Simple bootstrap function that intialises the app and any config
    """
    app = Flask(__name__)

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
