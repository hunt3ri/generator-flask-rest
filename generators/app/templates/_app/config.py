import logging


class EnvironmentConfig:
    """
    Environment Config contains values for the Dev, Test, Prod environments the app runs on.
    """
    DEBUG = False


class ProdConfig(EnvironmentConfig):
    DEBUG = False


class DevConfig(EnvironmentConfig):
    API_DOCS_URL = 'http://localhost:5000/docs/?url=http://localhost:5000/api/docs'
    DEBUG = True
    DYNAMODB_CONFIG = {
        'region_name': 'eu-west-1',
        'endpoint_url': 'https://dynamodb.eu-west-1.amazonaws.com'
    }
    LOG_DIR = 'logs'
    LOG_LEVEL = logging.DEBUG
