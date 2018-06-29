import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(base_dir, "data.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class Production(Config):
    DEBUG = False


class Development(Config):
    DEBUG = True
