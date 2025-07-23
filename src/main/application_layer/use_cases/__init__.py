import logging

from main.app import db
from contextlib import ContextDecorator

logger = logging.getLogger("auth." + __name__)


class transaction(ContextDecorator):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            db.session.rollback()
            logger.exception(f"Error: {exc_value}")
        else:
            db.session.commit()

        db.session.close()