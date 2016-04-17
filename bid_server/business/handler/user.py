#!/usr/bin/env python
# *_* coding=utf8 *_*

from bid_server.db import models
from bid_server.db.session import get_session
from bid_server.business.handler import base
from bid_server import app_config
import json

class LoginHandler(base.BaseHandler):

    def get(self):
        return self.render("user/login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        db_session = get_session()
        user = db_session.query(models.User).\
            filter_by(username=username).\
            filter_by(password=password).\
            first()

        if not user:
            self.set_error("帐号或密码错误！")
            self.render("user/login.html")

        if user.status != 0:
            self.set_error("用户被停用，请联系管理员！")
            self.render("user/login.html")

        self.set_user({
            'user_id': user.user_id,
            'username': user.username,
            'is_admin': user.is_admin
        })
        return self.redirect("/")


class LogoutHandler(base.BaseHandler):

    def get(self):
        self.logout()
        self.redirect("/login")


class IndexHandler(base.BaseHandler):

    @base.login
    def get(self):
        return self.render("index.html")


class ModifyPasswordHandler(base.BaseHandler):

    @base.login
    def get(self):
        return self.render("user/modify_password.html")

    @base.login
    def post(self):
        origin_password = self.get_argument("origin_password")
        password = self.get_argument("password")

        db_session = get_session()
        user = db_session.query(models.User).filter_by(
            user_id=self.user['user_id']).first()

        if user.password != origin_password:
            self.set_error("原始密码错误！")
            return self.render("user/modify_password.html")

        user.update({"password": password}).save(session=db_session)
        self.logout()

        return self.redirect("/login")
