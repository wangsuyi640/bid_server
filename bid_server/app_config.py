# *_* coding=utf8 *_*
#!/usr/bin/env python

from bid_server.db import models
from bid_server.db.session import get_session


def get(key, default=None):
    db_session = get_session()
    config = db_session.query(models.AppConfig)\
        .filter_by(key=key)\
        .filter_by(status=True)\
        .first()

    if config:
        return config.value
    else:
        return default


def set(key, value, create_by):
    db_session = get_session()
    config_list = db_session.query(models.AppConfig)\
        .filter_by(key=key)\
        .filter_by(status=True)\
        .all()

    for config in config_list:
        config.status = False
        config.save(session=db_session)

    models.AppConfig().update({
        "key": key,
        "value": value,
        "status": True,
        "create_by": create_by
    }).save()
