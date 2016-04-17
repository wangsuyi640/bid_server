#!/usr/bin/env python
# *_* coding=utf8 *_*

import os
import sys
import logging

__LOGGERS__ = {}
__LOGFILE_NAME__ = "%s.log" % os.path.basename(sys.argv[0])
__DEFAULT_PATH__ = '/var/log'


def gen_logger(name):

    formatter = logging.Formatter(
        '%(levelname)s: %(asctime)s %(funcName)s(%(lineno)d) -- %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(name)

    log_path = os.path.join(__DEFAULT_PATH__, __LOGFILE_NAME__)
    fh = logging.FileHandler(log_path)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.setLevel(logging.DEBUG)

    return logger


def get_logger(name):
    global __LOGGERS__
    logger = __LOGGERS__.get(name, None)
    if logger is None:
        logger = gen_logger(name)
        __LOGGERS__.setdefault(name, logger)

    return logger


def setup(logfile=None, path=None):
    global __LOGFILE_NAME__, __DEFAULT_PATH__
    if logfile:
        __LOGFILE_NAME__ = logfile

    if path:
        __DEFAULT_PATH__ = path
