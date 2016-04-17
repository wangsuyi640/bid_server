# *_* coding=utf8 *_*
#!/usr/bin/env python

import eventlet
eventlet.monkey_patch()

import time
import json
import socket
import logging
from xmlrpclib import ServerProxy
from bid_server import utils
from bid_server import config
from bid_server import exception
from bid_server.proto import *


GREEN_POOL = eventlet.GreenPool(1024)
logging.basicConfig(
    filename="/var/log/bid-%s.log" % (time.strftime('%Y-%m-%d_%H:%M:%S')), level=logging.DEBUG, filemode='w+',
    format='%(asctime)s - %(levelname)s: %(message)s')


class Event:

    def __init__(self, event_type, data):
        self.event_type = event_type
        self.data = data


class EventType:
    # 接收到客户端请求
    RECV_NETWORK_MSG = 1
    # 用户会话检查定时器
    SESSION_CHECK_TIMER = 2
    # 用户退出事件
    SESSION_QUIT = 3
    # 向用户发送价格更新信息
    UPDATE_PRICE_TIMER = 4


class YayaSession(object):

    """ 代表一个客户端会话 """

    def __init__(self, parent_server, client_addr, bid_no):
        self.parent_server = parent_server
        self.client_addr = client_addr
        self.bid_no = bid_no

        self.started = False
        self.looping_call = None
        self.loop_thread = None
        self.event_queue = eventlet.Queue()
        self.last_heartbeart_time = time.time()

    def recv_network_msg(self, msg):
        """
        客户端接收到网络消息
        Parameters:
            msg : YayaMessage
        """
        evt = Event(EventType.RECV_NETWORK_MSG, msg)
        self.event_queue.put(evt)

    def event_loop(self):
        """ 事件循环 """
        try:
            while 1:
                evt = self.event_queue.get()
                # 接收到网络消息
                if evt.event_type == EventType.RECV_NETWORK_MSG:
                    msg = evt.data
                    # 心跳包
                    if type(msg) is HelloClientMessage:
                        self.last_heartbeart_time = time.time()

                # 会话检查定时器
                elif evt.event_type == EventType.SESSION_CHECK_TIMER:
                    expire_seconds = time.time() - self.last_heartbeart_time
                    if expire_seconds > config.SESSION_EXPIRE_SECONDS:
                        SESSION_QUIT_evt = Event(
                            EventType.SESSION_QUIT, self.client_addr)
                        self.parent_server.send_evt(SESSION_QUIT_evt)

        except exception.StopEventLoop:
            pass

    def start(self):
        """ 开始执行客户端循环 """
        if not self.started:
            self.started = True
            self.looping_call = utils.LoopingCall(
                lambda: self.event_queue.put(
                    Event(EventType.SESSION_CHECK_TIMER, None)
                )
            )
            self.looping_call.start(config.SESSION_EXPIRE_SECONDS / 2)
            self.loop_thread = GREEN_POOL.spawn(self.event_loop)

    def stop(self):
        """ 结束事件循环 """
        if self.started:
            self.started = False
            self.looping_call.stop()
            eventlet.kill(self.loop_thread,
                          exception.StopEventLoop)

            self.looping_call = None
            self.loop_thread = None


class PriceUpdater(object):

    """ 价格更新器（接收客户端发来的价格，在合适的时机转发给其他客户端） """

    def __init__(self, parent_server):
        self.started = False
        self.event_thread = None
        self.looping_call = None

        self.max_price = 100
        self.max_price_time = '00:00:00'
        self.current_price_list = []
        self.rpc_proxy = ServerProxy("http://127.0.0.1:%s" % config.RPC_PORT)

        self.event_queue = eventlet.Queue()
        self.parent_server = parent_server

    def feed_price(self, update_time, price):
        # self.current_price_list.append(
        #     (update_time, price))
        pass

    def broadcast_price(self):
        resp = json.loads(self.rpc_proxy.get_price())

        # 时间以服务器的时间为准哦
        update_time = time.strftime('%H:%M:%S')
        msg = MyBidInfoMessage(update_time, resp['price'])
        self.parent_server.broadcast(msg)



    def send_evt(self, evt):
        self.event_queue.put(evt)

    def event_loop(self):
        """ 事件循环 """
        try:
            while 1:
                evt = self.event_queue.get()

                if evt.event_type == EventType.RECV_NETWORK_MSG:
                    msg = evt.data
                    if type(msg) is UpdatePriceMessage:
                        self.feed_price(msg.update_time, msg.price)

                elif evt.event_type == EventType.UPDATE_PRICE_TIMER:
                    self.broadcast_price()

        except exception.StopEventLoop:
            pass

    def start(self):
        """
        开始事件循环
        """
        if not self.started:
            self.started = True
            self.looping_call = utils.LoopingCall(
                lambda: self.send_evt(
                    Event(EventType.UPDATE_PRICE_TIMER, None)
                )
            )
            self.looping_call.start(0.5)
            self.event_thread = GREEN_POOL.spawn(self.event_loop)

    def stop(self):
        """
        结束
        """
        if self.started:
            self.started = False

            self.looping_call.stop()
            eventlet.kill(
                self.event_thread, exception.StopEventLoop)

            self.looping_call = None
            self.event_thread = None


class YayaUDPServer(object):

    """ UDP server """

    def __init__(self):
        self.started = False
        self.event_thread = None
        self.recv_thread = None
        self.send_thread = None

        self.sessions = {}
        self.event_queue = eventlet.Queue()
        self.send_msg_queue = eventlet.Queue()
        self.price_updater = PriceUpdater(self)

        self.listen_port = config.UDP_PORT
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_sock.bind(('', self.listen_port))

    def start(self):
        if not self.started:
            self.started = True
            self.event_thread = GREEN_POOL.spawn(self.event_loop)
            self.send_thread = GREEN_POOL.spawn(self.send_loop)
            self.recv_loop = GREEN_POOL.spawn(self.recv_loop)
            self.price_updater.start()

    def stop(self):
        if self.started:
            self.started = False
            self.price_updater.stop()
            eventlet.kill(self.recv_loop, exception.StopEventLoop)
            self.recv_loop = None
            eventlet.kill(self.event_thread, exception.StopEventLoop)
            self.event_thread = None
            eventlet.kill(self.send_thread, exception.StopEventLoop)
            self.send_thread = None

    def unicast(self, addr, msg):
        """ 向单个会话进行消息单播 """
        self.send_msg_queue.put((addr, msg))

    def broadcast(self, msg):
        """ 向所有的会话进行消息广播 """
        for addr in self.sessions.keys():
            print "broadcast all client:%s" % (msg)
            self.send_msg_queue.put((addr, msg))

    def send_evt(self, evt):
        self.event_queue.put(evt)

    def recv_loop(self):
        """ 接收网络消息，并进行消息分配的循环 """

        try:
            while 1:
                raw_msg, addr = self.server_sock.recvfrom(1024)
                print raw_msg
                try:
                    msg = YayaMessage.from_raw(raw_msg)
                    msg_type = type(msg)
                    session = self.sessions.get(addr)
                    if not session:
                        if type(msg) is HelloClientMessage:
                            self.create_session(addr, msg)
                        continue

                    if type(msg) is UpdatePriceMessage:
                        logging.info(
                            "%s --> UpdatePriceMessage:%s" % (addr, msg))
                        self.price_updater.send_evt(
                            Event(EventType.RECV_NETWORK_MSG, msg))
                    else:
                        session.recv_network_msg(msg)

                except exception.IllegalNetworkMessage:
                    print "exception.IllegalNetworkMessage"
                    pass
                except exception.UnkownYayaMessage:
                    print "exception.UnkownYayaMessage"
                    pass

        except exception.StopEventLoop:
            pass

    def send_loop(self):
        """ 发送网络消息的循环 """

        try:
            while 1:
                addr, msg = self.send_msg_queue.get()
                logging.info('Send message (%s,%s)' % (addr, msg))
                content = None
                if isinstance(msg, YayaMessage):
                    content = msg.to_raw()
                elif type(msg) is str:
                    content = msg

                if content:
                    self.server_sock.sendto(content, addr)

        except exception.StopEventLoop:
            pass

    def event_loop(self):
        """ 事件循环 """
        try:
            while 1:
                evt = self.event_queue.get()
                if evt.event_type == EventType.SESSION_QUIT:
                    client_addr = evt.data
                    self.delete_session(client_addr)

        except exception.StopEventLoop:
            pass

    def create_session(self, client_addr, hello_message):
        """
        创建用户会话
        Parameters:
            client_addr : 用户Address (ip, port)
        """
        print 'Create session'
        session = YayaSession(self, client_addr, hello_message.bid_no)
        self.sessions[client_addr] = session
        session.start()

        return session

    def delete_session(self, client_addr):
        """
        删除用户会话
        Parameters:
            client_addr : 用户Address (ip, port)
        """
        print 'Delete session'
        session = self.sessions.get(client_addr)
        if session:
            session.stop()
            del self.sessions[client_addr]


def wait():
    GREEN_POOL.waitall()
