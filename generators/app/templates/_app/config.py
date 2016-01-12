class Config(object):
    DEBUG = False


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'iain-test',
        'host': '192.168.99.100',
        'port': 27017
    }