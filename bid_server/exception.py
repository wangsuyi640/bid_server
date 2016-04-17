# *_* coding=utf8 *_*
#!/usr/bin/env python


class YayaException(Exception):

    """ Base Exception of all self defined exceptions. """
    message = "Unkown Yaya Exception"

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __str__(self):
        print self.kwargs
        return self.message.format(**self.kwargs)


class StopEventLoop(YayaException):

    """ Throw it to a eventlet green thread for stop it. """
    pass


class IllegalNetworkMessage(YayaException):
    message = "Unlegal Network Message"


class UnkownYayaMessage(YayaException):
    message = "Unkown Yaya Message({raw_message})"
