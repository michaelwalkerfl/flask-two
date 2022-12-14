import os
import redis

from webapp.utils import parse_env

base_directory = os.path.abspath(os.path.dirname(__file__))

parse_env()


class Config:
    # Flask
    APP_NAME = os.environ.get('APP_NAME', 'Flask-Two')
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'SET_YOUR_SECRET_KEY')
    JSONIFY_PRETTYPRINT_REGULAR = True

    # Database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'redis')
    SESSION_REDIS = redis.from_url(os.environ.get(
        'SESSION_REDIS', 'redis://localhost:6379')
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOPMENT_DATABASE',
        'sqlite:///' + os.path.join(base_directory, 'development-database.sqlite')
    )

    @classmethod
    def init_app(cls, app):
        print('APPLICATION IS IN DEVELOPMENT MODE.')


class TestsConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOPMENT_DATABASE',
        'sqlite:///' + os.path.join(base_directory, 'tests-database.sqlite')
    )
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        print('APPLICATION IS IN TEST MODE.')


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEVELOPMENT_DATABASE',
        'sqlite:///' + os.path.join(base_directory, 'production-database.sqlite')
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class UbuntuConfig(ProductionConfig):

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'test': TestsConfig,
    'production': ProductionConfig,
    'ubuntu': UbuntuConfig,
}
