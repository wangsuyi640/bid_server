#!/usr/bin/env python
# *_* coding=utf8 *_*

from bid_server.db import models
from bid_server.db.session import get_session
from bid_server.business.handler import base
from bid_server import app_config
import json

class LogInfoHandler(base.BaseHandler):

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        login_url = app_config.get('login_url', 'NA')
        bid_url = app_config.get('bid_url', 'NA')
        priceInputRight = app_config.get('priceInputRight', 0)
        priceInputBottom = app_config.get('priceInputBottom', 0)
        preBidRight = app_config.get('preBidRight', 0)
        preBidBottom = app_config.get('preBidBottom', 0)
        bidRight = app_config.get('bidRight', 0)
        bidBottom = app_config.get('bidBottom', 0)

        # 这个长度10是随便写的

        resp = {
            'login_url': login_url,
            'bid_url': bid_url,
            'priceInputRight': priceInputRight,
            'priceInputBottom': priceInputBottom,
            'preBidRight': preBidRight,
            'preBidBottom': preBidBottom,
            'bidRight': bidRight,
            'bidBottom': bidBottom

        }
        print resp
        self.write(json.dumps(resp))

    def post(self):
        pass


class TestInfoHandler(base.BaseHandler):

    def get(self):
        test_start_time = app_config.get('test_start_time', 'NA')
        test_mid_time = app_config.get('test_mid_time', 'NA')
        test_end_time = app_config.get('test_end_time', 'NA')
        test_bid_time = app_config.get('test_bid_time', 'NA')

        resp = {
            'test_start_time': test_start_time,
            'test_mid_time': test_mid_time,
            'test_end_time': test_end_time,
            'test_bid_time': test_bid_time
        }
        print resp
        self.write(json.dumps(resp))

    def post(self):
        pass