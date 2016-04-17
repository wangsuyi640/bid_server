#!/usr/bin/env python
# *_* coding=utf8 *_*

class _RpcAPI(object):

    def __init__(self):
        self.functions = {}

    def api(self, rpc_func):
        func_name = rpc_func.__name__
        self.functions[func_name] = rpc_func
        return rpc_func

    def import_api(self):
        from bid_server.api import lottery
        from bid_server.api import mock

    def get_func(self, func_name):
        return self.functions.get(func_name)

    def get_all_funcs(self):
        return self.functions


RpcAPI = _RpcAPI()


