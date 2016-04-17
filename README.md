# bid-server - v1.0

* Just init.

## 1. Introduction

A fork of bid. bid-server

### Technology:

The application logic is written in Python & Tornado.

### License

bid-server is licensed under the LGPL Licence.

## 2. Installation

### 1) RHEL 6.5 or CentOS 6.5

#### install python2.7
    # cd /etc/yum.repos.d/
    # wget  http://people.redhat.com/bkabrda/scl_python27.repo 
	# mv scl_python27.repo scl.repo
	# yum install python27
	# scl enable python27 bash

#### install bid-server
	# git clone https://github.com/wangsuyi640/bid_server.git
	# cd bid-server
	# python setup.py install


### 2) Ubuntu 12.04 or above
#### install redis server
	# apt-get install redis-server
#### install bid-server
	# git clone https://github.com/wangsuyi640/bid_server.git
	# cd bid-server
	# python setup.py install

## 3. 启动服务

### 1) 先启动 bid-rpc-server


### 2) 再启动 bid-udp-server