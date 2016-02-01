class ApplicationConfig:
    """
    Application wide config, these values can't be different in Dev, Test, Live.  Typically used for values that
    need to be read when modules are being initialised.
    """
    DATABASE_ENGINE = 'mongo'


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
    MONGODB_SETTINGS = {
        'db': 'iain-test',
        'host': '192.168.99.100',
        'port': 27017
    }