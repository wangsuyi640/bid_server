#!/usr/bin/env python
# *_* coding=utf8 *_*

import time
import json
from bid_server import app_config
from bid_server.api import RpcAPI



@RpcAPI.api
def update_price(update_time, price):
    app_config.set("price", price, 1)
    app_config.set("update_time", update_time, 1)
    print price
    return json.dumps({
        'result': 0
    })

@RpcAPI.api
def get_price():
    price = app_config.get("price", None)
    update_time = app_config.get("update_time", None)
    return json.dumps({
        'price': price,
        'update_time': update_time
    })