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
    LOG_DIR = 'logs'
    LOG_LEVEL = logging.DEBUG
    MONGODB_SETTINGS = {
        'db': 'iain-test',
        'host': '192.168.99.100',
        'port': 27017
    }
