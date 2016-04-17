#!/usr/bin/env python
# *_* coding=utf8 *_*

import os
import redis
import tornado
from tornado import web
from tornado import httpserver

from bid_server import config
from bid_server.redis_session import RedisSessionStore
from bid_server.business.handler import user, admin, client


class Application(web.Application):

    def __init__(self):

        handlers = [
            (r"/", user.IndexHandler),
            (r"/login", user.LoginHandler),
            (r"/logout", user.LogoutHandler),

            (r"/admin/user", admin.UserHandler),
            (r"/admin/add_user", admin.AddUserHandler),
            (r"/admin/modify_user", admin.ModifyUserHandler),
            (r"/admin/app_config", admin.AppConfig),
            (r"/admin/testinfo_config", admin.TestInfoConfig),
            (r"/modify_password", user.ModifyPasswordHandler),

            # for Csharp client
            (r"/get_login_info", client.LogInfoHandler),
            (r"/get_test_info", client.TestInfoHandler),
        ]

        redis_connection = redis.Redis(host=config.SESSION_REDIS_HOST,
                                       port=config.SESSION_REDIS_PORT,
                                       db=config.SESSION_REDIS_DB)

        self.session_store = RedisSessionStore(redis_connection)

        application_settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='You would never know this',
            debug=config.IS_DEBUG)

        web.Application.__init__(self, handlers=handlers, **application_settings)


def start():
    http_server = httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(config.BUSINESS_PORT)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    start()
