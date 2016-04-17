#!/usr/bin/env python
# *_* coding=utf8 *_*

from sqlalchemy import func
from bid_server.db import models
from bid_server import app_config
from bid_server.db.session import get_session
from bid_server.business.handler import base
import time

class UserHandler(base.BaseHandler):

    @base.admin
    def get(self):
        db_session = get_session()

        users = db_session.query(
            models.User,
            func.count(func.distinct(models.LicenseRecord.bid_no)).label(
                'download_license_count')
        ).outerjoin(
            models.LicenseRecord, models.User.user_id == models.LicenseRecord.user_id
        ).group_by(models.User.user_id).all()

        return self.render("admin/user_list.html", users=users)


class AddUserHandler(base.BaseHandler):

    @base.admin
    def get(self):
        return self.render("admin/add_user.html")

    @base.admin
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        remark = self.get_argument("remark")
        is_admin = self.get_argument("is_admin", None)

        db_session = get_session()

        user = db_session.query(models.User).filter_by(
            username=username).first()

        if user:
            self.set_error("用户名已经存在。")
            return self.render("admin/add_user.html")

        models.User().update({
            "username": username,
            "password": password,
            "remark": remark,
            "is_admin": 1 if is_admin else 0,
            "create_by": self.user['user_id'],
            "status": 0,
        }).save()

        return self.redirect("/admin/user")


class ModifyUserHandler(base.BaseHandler):

    @base.admin
    def get(self):
        try:
            user_id = int(self.get_argument("user_id", None))
        except:
            return self.render_prompts(type="error", text="参数错误")

        db_session = get_session()
        user = db_session.query(models.User).filter_by(
            user_id=user_id).first()

        if not user:
            return self.render_prompts(type="error", text="该用户不存在")

        return self.render("admin/modify_user.html", user=user)

    @base.admin
    def post(self):
        user_id = int(self.get_argument("user_id"))
        password = self.get_argument("password")
        remark = self.get_argument("remark")
        is_admin = self.get_argument("is_admin", None)
        status = self.get_argument("status")

        db_session = get_session()
        user = db_session.query(models.User).filter_by(
            user_id=user_id).first()

        if not user:
            return self.render_prompts(type="error", text="该用户不存在")

        user.update({
            "remark": remark,
            "is_admin": True if is_admin else False,
            "status": 0 if int(status) == 0 else 1
        })

        if password:
            user.update(dict(password=password))

        user.save(session=db_session)

        return self.redirect("/admin/user")

class AppConfig(base.BaseHandler):

    @base.admin
    def get(self):
        return self.render("admin/app_config.html")

    @base.admin
    def post(self):
        key = self.get_argument("key")
        value = self.get_argument("value")

        if not value:
            self.set_error(u"%s不能为空" % key)
            return self.render("admin/app_config.html")

        value_old = app_config.get(key, None)
        if value == value_old:
            return self.render("admin/app_config.html")

        app_config.set(key, value, self.user['user_id'])

        return self.render("admin/app_config.html")

class TestInfoConfig(base.BaseHandler):

    def _is_valid_time(self, timestr):
        try:
            time.strptime(timestr, "%H:%M:%S")
            return True
        except:
            return False

    @base.admin
    def get(self):
        return self.render("admin/testinfo_config.html")

    @base.admin
    def post(self):
        key = self.get_argument("key")
        value = self.get_argument("value")

        if not value:
            self.set_error(u"%s不能为空" % key)
            return self.render("admin/testinfo_config.html")

        if not self._is_valid_time(value):
            format_info = "%H:%M:%S"
            self.set_error(u"%s 时间格式不对！请遵循格式：%s" % (key, format_info))
            return self.render("admin/testinfo_config.html")

        value_old = app_config.get(key, None)
        if value == value_old:
            return self.render("admin/testinfo_config.html")

        app_config.set(key, value, self.user['user_id'])

        return self.render("admin/testinfo_config.html")