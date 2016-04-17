#!/usr/bin/env python
# *_* coding=utf8 *_*

import re
from bid_server.api import RpcAPI

@RpcAPI.api
def hello():
    print 'hit 1'
    return "hello world"

@RpcAPI.api
def hello2():
    return "hello world2"

@RpcAPI.api
def get_ifs(self, filter_local = False):
    try:
        res = self._run_programme("ifconfig -a | sed 's/[ :\t].*//;/^\\(\\)$/d'")
        stat = res[0]
        ifs = []
        output = []
        if stat == 0:
            ifs = res[1].split('\n')
        ifs = sorted(set(ifs))
        if filter_local:
            for s in ifs:
                if s:
                    match = re.match('lo\\d', s, re.I)
                    if match:
                        print('local loopback device located, skipping.')
                    else:
                        output.append(s)

        else:
            output = ifs
        return output
    except Exception as e:
        print str(e)