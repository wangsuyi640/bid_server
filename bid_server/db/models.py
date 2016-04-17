#!/usr/bin/env python
# *_* coding=utf8 *_*

from bid_server.db.session import get_session
from sqlalchemy import Column, DateTime, String, Integer, Unicode, func, schema
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class YayaBase(object):

    def save(self, session=None):
        """Save this object."""
        if not session:
            session = get_session()
        session.add(self)
        session.flush()

    def update(self, values):
        """Make the model object behave like a dict"""
        for k, v in values.iteritems():
            setattr(self, k, v)

        return self

    def iteritems(self):
        """Make the model object behave like a dict.

        Includes attributes from joins."""
        local = dict(self)
        joined = dict([(k, v) for k, v in self.__dict__.iteritems()
                      if not k[0] == '_'])
        local.update(joined)
        return local.iteritems()

    def get(self, key):
        return self.__dict__.get(key)


class User(Base, YayaBase):

    """ 用户表 """
    __tablename__ = "user"
    __table_args__ = (schema.UniqueConstraint("username"),)

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    create_time = Column(DateTime, default=func.now())
    # 由哪个用户创建了该用户
    create_by = Column(Integer)
    # 是否为管理员
    is_admin = Column(Integer)
    # 用户备注
    remark = Column(String)
    # 用户状态
    status = Column(Integer)


class LicenseRecord(Base, YayaBase):

    """ 用户下载记录 """
    __tablename__ = "license_record"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    bid_no = Column(String)
    file_content = Column(Unicode)
    password = Column(String)
    clientname = Column(String)
    pin_no = Column(String)
    create_time = Column(DateTime, default=func.now())


class LoginRecord(Base, YayaBase):

    """ 用户登录记录 用以绑定MAC地址 """
    __tablename__ = "login_record"
    __table_args__ = (schema.UniqueConstraint("mac_address"),)

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    bid_no = Column(String)
    mac_address = Column(String)
    create_time = Column(DateTime, default=func.now())
    login_count = Column(Integer)
    last_login_time = Column(DateTime)


class AppConfig(Base, YayaBase):

    """ 程序配置表 """
    __tablename__ = "app_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    value = Column(String)
    status = Column(Integer)
    create_by = Column(Integer)
    create_time = Column(DateTime, default=func.now())
