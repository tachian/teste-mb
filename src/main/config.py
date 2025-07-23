import logging
import os

from dotenv import load_dotenv

import json

load_dotenv()


class BaseConfig(object):

    DEBUG = False
    TESTING = False
    DEPLOY_ENV = os.environ.get('DEPLOY_ENV', 'Development')
    LOGS_LEVEL = logging.INFO
    RESTPLUS_VALIDATE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'sqlite:///addresses.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOGS_LEVEL = logging.CRITICAL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'sqlite:///addresses-test.db')
class StagingConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = int(os.environ.get('LOG_LEVEL', default=logging.INFO))
