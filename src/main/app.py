import os
import sys
import logging

import json_logging
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from main.presentation_layer import install_error_handlers
from sqlalchemy import MetaData
from web3 import Web3




ENV = os.environ.get('DEPLOY_ENV', 'Development')

convention = {
    "ix": "ix_%(column_0_label)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
    "uq": "%(table_name)s_%(column_0_name)s_key"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))


def create_app(deploy_env: str = ENV) -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f'main.config.{deploy_env}Config')

    __register_blueprints_and_error_handling(app)
    __configure_logger(app)
    __register_commands(app)

    db.init_app(app)
    Migrate(app, db)

    

    return app

def __register_blueprints_and_error_handling(app: Flask):
    from main.presentation_layer.views.api import blueprint

    app.register_blueprint(blueprint)

    error_codes = [400, 401, 403, 404, 405, 406, 408, 409, 410, 412,
                   415, 428, 429, 500, 501]
    install_error_handlers(error_codes, app)


def __configure_logger(app: Flask):
    if not json_logging.ENABLE_JSON_LOGGING:
        json_logging.init_flask(enable_json=True)
        json_logging.init_request_instrument(app)

    logger = logging.getLogger("teste-mb")
    logger.setLevel(app.config["LOGS_LEVEL"])
    logger.addHandler(logging.StreamHandler(sys.stdout))


def __register_commands(app):
    from main.commands import drop_create_tables

    app.cli.command("drop-create-tables")(drop_create_tables)



