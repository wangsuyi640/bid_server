# *_* coding=utf8 *_*

"""
描述：Bid server 安装脚本
"""

import os
import setuptools
import sys

requirements = [
    "rsa",
    "eventlet==0.15.2",
    "tornado==4.0",
    "sqlalchemy",
    "redis",
    "xlrd"
]

setuptools.setup(
    name="bid_server",
    version="2015.7",
    author="Tang",
    description="Bid server for paipai.",
    packages=setuptools.find_packages(exclude=['tests', 'bin']),
    scripts=[
        'bin/bid-udp-server',
        'bin/bid-web',
        'bin/bid-rpc-server'
    ],
    install_requires=requirements,
)
