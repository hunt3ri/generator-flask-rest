from flask import Flask

def bootstrap_app():
    """
    Simple bootstrap function that intialises the app and any config
    """
    app = Flask(__name__)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
