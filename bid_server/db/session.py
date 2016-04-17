#!/usr/bin/env python
# *_* coding=utf8 *_*

"""Session Handling for SQLAlchemy backend."""

import sqlalchemy.exc
import sqlalchemy.orm
import time

from bid_server import config


_ENGINE = None
_MAKER = None


def get_session(autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy session."""
    global _ENGINE, _MAKER

    if _MAKER is None or _ENGINE is None:
        _ENGINE = get_engine()
        _MAKER = get_maker(_ENGINE, autocommit, expire_on_commit)

    session = _MAKER()
    return session


def get_engine():
    """Return a SQLAlchemy engine."""
    connection_dict = sqlalchemy.engine.url.make_url(config.DB_CONNECTION)

    engine_args = {
        "pool_recycle": config.SQL_IDLE_TIMEOUT,
        "echo": False,
    }

    if "sqlite" in connection_dict.drivername:
        engine_args["poolclass"] = sqlalchemy.pool.NullPool

    engine = sqlalchemy.create_engine(config.DB_CONNECTION, **engine_args)
    return engine


def ensure_connection(engine):
    remaining_attempts = config.MAX_DB_RETRY_TIMES
    while True:
        try:
            engine.connect()
            return
        except sqlalchemy.exc.OperationalError:
            if remaining_attempts == 0:
                raise
            time.sleep(config.SQL_RETRY_INTERVAL)
            remaining_attempts -= 1


def get_maker(engine, autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy sessionmaker using the given engine."""
    return sqlalchemy.orm.sessionmaker(bind=engine,
                                       autocommit=autocommit,
                                       expire_on_commit=expire_on_commit)
