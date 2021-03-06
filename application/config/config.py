# -*- coding: utf-8 -*-
import os, json

class Config(object):
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_PASSWORD_HASH = os.environ.get('SECURITY_PASSWORD_HASH', 'bcrypt')

    HOST = os.environ.get('HOST', 'localhost')

    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI')
    }

    LRS_HOST = os.environ.get('LRS_HOST')
    LRS_PORT = os.environ.get('LRS_PORT')
    LRS_HTTPS_ENABLED = json.loads(os.environ.get('LRS_HTTPS_ENABLED', 'false'))
    LRS_USER = os.environ.get('LRS_USER')
    LRS_PASS = os.environ.get('LRS_PASS')
    LRS_QUERY_API_URL = os.environ.get('LRS_QUERY_API_URL')
    LRS_COMMAND_API_URL = os.environ.get('LRS_COMMAND_API_URL')
    LRS_QUERY_URL = os.environ.get('LRS_QUERY_URL')
    LRS_STATEMENTS_URL = os.environ.get('LRS_STATEMENTS_URL')

    DGN_RULE = os.environ.get('DGN_RULE', 'learning_registry_match')

    LR_URL = os.environ.get('LR_URL', 'http://sandbox.learningregistry.org')
    LR_QUERY_URL = os.environ.get('LR_QUERY_URL', '/slice?any_tags=civil%20service%20learning')

    OPEN_LRS_HOST = os.environ.get('OPEN_LRS_HOST')
    OPEN_LRS_COMMAND_PORT = os.environ.get('OPEN_LRS_COMMAND_PORT')
    OPEN_LRS_QUERY_PORT = os.environ.get('OPEN_LRS_QUERY_PORT')
    OPEN_LRS_HTTPS_ENABLED = json.loads(os.environ.get('OPEN_LRS_HTTPS_ENABLED', 'false'))
    OPEN_LRS_USER = os.environ.get('OPEN_LRS_USER')
    OPEN_LRS_PASS = os.environ.get('OPEN_LRS_PASS')

    OPEN_LRS_COMMAND_URL = os.environ.get('OPEN_LRS_COMMAND_URL')
    OPEN_LRS_QUERY_URL = os.environ.get('OPEN_LRS_QUERY_URL')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = Config.SECRET_KEY or 'local-dev-not-secret'


class TestConfig(DevelopmentConfig):
    TESTING = True
