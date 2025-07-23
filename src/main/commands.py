import flask_migrate
from flask.cli import with_appcontext
from flask import current_app

from main.app import db


class InvalidEnvironment(Exception):
    pass


def _drop_tables():
    with db.get_engine().begin() as conn:
        
        for row in result:
            conn.execute(f'drop table {row[0]} CASCADE;')

def _drop_create_tables():
    _drop_tables()
    db.session.commit()
    flask_migrate.upgrade()
    db.session.commit()

@with_appcontext
def drop_create_tables():
    if current_app.config["DEPLOY_ENV"] == 'Production':
        raise InvalidEnvironment('Drop/Create tables unable for production')
    _drop_create_tables()
    
