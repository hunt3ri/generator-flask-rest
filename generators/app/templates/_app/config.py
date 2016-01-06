class Config(object):
    DEBUG = False


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True