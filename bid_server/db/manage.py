#!/usr/bin/env python
# *_* coding=utf8 *_*

from bid_server import config
from bid_server.db import models
from bid_server.db.session import get_engine


def create_all():
    engine = get_engine()
    models.Base.metadata.create_all(engine)


def init_admin_user():
    models.User().update({
        "username": "admin",
        "password": config.ADMIN_INIT_PASSWORD,
        "create_all": None,
        "is_admin": True,
        "remark": u"系统初始化帐号",
        "status": 0,
    }).save()

if __name__ == "__main__":
    create_all()
    init_admin_user()
