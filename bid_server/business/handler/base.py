#!/usr/bin/env python
# *_* coding=utf8 *_*

from bid_server import config
from bid_server import redis_session
from tornado.web import RequestHandler, HTTPError


def login(handler_func):
    def wrapper(handler, *args, **kwargs):
        if handler.user is not None:
            return handler_func(handler, *args, **kwargs)
        else:
            return handler.redirect("/login")

    return wrapper


def admin(handler_func):
    def wrapper(handler, *args, **kwargs):
        if handler.user is None:
            return handler.redirect("/login")
        elif not handler.user['is_admin']:
            return handler.write("<h2>需要管理员权限。</h2>")
        else:
            return handler_func(handler, *args, **kwargs)

    return wrapper


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.prompts = {
            "error": [],
            "info": []
        }

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            sessionid = self.get_secure_cookie('session_id')
            self._session = redis_session.RedisSession(
                self.application.session_store,
                sessionid, expires_days=config.SESSION_PERMAMENT_DAYS)

            if not sessionid:
                self.set_secure_cookie(
                    'session_id', self._session.id,
                    httponly=True, expires_days=None)

        return self._session

    def set_user(self, user):
        self.session['user'] = user
        self.session.save()

    def logout(self):
        self.session['user'] = None
        self.session.save()

    @property
    def user(self):
        if not hasattr(self, '__user__'):
            user = self.session.get('user')
            setattr(self, '__user__', user)

        return self.__user__

    def set_error(self, error):
        self.prompts['error'].append(error)

    def set_info(self, info):
        self.prompts['info'].append(info)

    def render_prompts(self, type="info", text=""):
        return self.render("info.html", type=type, text=text)
