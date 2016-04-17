# *_* coding=utf8 *_*
#!/usr/bin/env python

import re
import struct

from urllib import unquote
from bid_server import utils
from bid_server import exception

# ------------------------ Network Message Encode/Decode ---------------------

"""
编码说明：本地使用UTF-8编码，网络上统一使用GB2312编码。
"""

to_hex = lambda x: ':'.join([hex(ord(c))[2:].zfill(2) for c in x])


class NetworkMessageParser:

    """ Yaya network proto with bid client """

    @staticmethod
    def decode(data):
        """ Decode UDP msg with bid client """

        def decode_udp(udp_raw):
            udp_conv = ''
            for e in udp_raw.split(':'):
                e_hex = int(e, 16)
                e_hex_xor = e_hex ^ 255
                e_hex_xor_rep = format(e_hex_xor, '02x')
                udp_conv += '%' + e_hex_xor_rep
                udp_msg = unquote(udp_conv)

            return udp_msg

        def parse_udp_msg(data):
            raw_udp_list = [data[i:i + 2] for i in range(0, len(data), 2)]
            raw_udp = ':'.join(raw_udp_list)
            msg = decode_udp(raw_udp)
            return msg

        local_msg = parse_udp_msg(data.encode('hex_codec'))
        return local_msg

    @staticmethod
    def encode(data):
        """ Encode UDP msg with bid client """

        def encode_udp(udp_raw):
            udp_raw = to_hex(udp_raw)
            udp_conv = ''
            for e in udp_raw.split(':'):
                e_hex = int(e, 16)
                e_hex_xor = e_hex ^ 255
                e_hex_xor_rep = format(e_hex_xor, '02x')
                udp_conv += struct.pack('B', e_hex_xor)

            return udp_conv

        # return encode_udp(data)
        return data


# -------------------------- YaYa Message Proto ---------------------------

TIME_RE = re.compile(r'^\d{2}:\d{2}:\d{2}$')
INT_RE = re.compile(r'^\d+$')


class YayaMessageType:

    CLIENT_MSG = "CLIENT"
    FORMAT_MSG = "FORMAT"
    UPDATE_MSG = "UPDATE"
    INFO_MSG = "INFO"


class YayaMessage(object):

    """ Network Message """

    type_part_re = re.compile(r'<TYPE>(.*)</TYPE>', re.IGNORECASE)
    msg_type = None

    def __init__(self, msg):
        self.__msg__ = msg

    @classmethod
    def from_raw(cls, raw):
        # try:
        #     msg_content = NetworkMessageParser.decode(raw)
        # except:
        #     raise exception.IllegalNetworkMessage()

        msg_content = raw
        matched_groups = cls.type_part_re.search(msg_content)
        if matched_groups:
            msg_type = matched_groups.group(1)
        else:
            msg_type = None

        msg_cls_list = MESSAGE_MAP.get(msg_type, [])
        for msg_cls in msg_cls_list:
            msg = msg_cls.from_msg(msg_content)
            if msg:
                return msg

        raise exception.UnkownYayaMessage(raw_message=msg_content)

    @classmethod
    def from_msg(cls, msg):
        raise NotImplemented()

    def __repr__(self):
        return "%s('%s')" % (type(self), self.to_msg())

    def to_msg(self):
        return self.__msg__

    def to_raw(self):
        return NetworkMessageParser.encode(self.to_msg())


class HelloClientMessage(YayaMessage):

    """ 作为用户信息认证和格式请求的Message """

    msg_type = YayaMessageType.CLIENT_MSG
    bid_no_re = re.compile(r'<BIDNO>(.*)</BIDNO>', re.IGNORECASE)
    vcode_re = re.compile(r'<VCODE>(.*)</VCODE>', re.IGNORECASE)

    def __init__(self, bid_no, vcode):
        self.bid_no = bid_no
        self.vcode = vcode

    @classmethod
    def from_msg(cls, msg):
        bid_no_groups = cls.bid_no_re.search(msg)
        vcode_groups = cls.vcode_re.search(msg)

        if bid_no_groups and vcode_groups:
            return cls(bid_no_groups.group(1), vcode_groups.group(1))

        return None

    def to_msg(self):
        return "<TYPE>%s</TYPE><BIDNO>%s</BIDNO><VCODE>%s</VCODE>" % (
            self.msg_type, self.bid_no, self.vcode)


class HelloMessage(YayaMessage):

    """ 作为用户信息认证和格式请求的Message """

    msg_type = YayaMessageType.FORMAT_MSG
    bid_no_re = re.compile(r'<BIDNO>(.*)</BIDNO>', re.IGNORECASE)
    vcode_re = re.compile(r'<VCODE>(.*)</VCODE>', re.IGNORECASE)

    def __init__(self, bid_no, vcode):
        self.bid_no = bid_no
        self.vcode = vcode

    @classmethod
    def from_msg(cls, msg):
        bid_no_groups = cls.bid_no_re.search(msg)
        vcode_groups = cls.vcode_re.search(msg)

        if bid_no_groups and vcode_groups:
            return cls(bid_no_groups.group(1), vcode_groups.group(1))

        return None

    def to_msg(self):
        return "<TYPE>%s</TYPE><BIDNO>%s</BIDNO><VCODE>%s</VCODE>" % (
            self.msg_type, self.bid_no, self.vcode)


class FormatMessage(YayaMessage):

    """ 国拍返回的用于解释BidMessage的Message """

    msg_type = YayaMessageType.FORMAT_MSG
    info_re = re.compile(r'<INFO>(.*)</INFO>', re.IGNORECASE)

    def __init__(self, format_msg):
        self.format_msg = format_msg

    @classmethod
    def from_msg(cls, msg):
        info_groups = cls.info_re.search(msg)

        if info_groups:
            return cls(info_groups(1))

        return None

    def to_msg(self):
        return "<xml><TYPE>%s</TYPE><INFO>%s</INFO>" % (
            self.msg_type, self.format_msg)


class UpdatePriceMessage(YayaMessage):

    """ 客户端向服务端更新价格的Message """

    msg_type = YayaMessageType.UPDATE_MSG
    info_re = re.compile(r'<INFO>(.*)</INFO>', re.IGNORECASE)

    def __init__(self, update_time, price):
        self.update_time = update_time
        self.price = price

    @classmethod
    def from_msg(cls, msg):
        info_groups = cls.info_re.search(msg)

        if info_groups:
            info_str = info_groups.group(1)
            info_list = info_str.split('^')
            if len(info_list) == 2:
                update_time = info_list[0]
                price = info_list[1]

                if TIME_RE.match(update_time) and INT_RE.match(price):
                    return cls(update_time, price)

        return None

    def to_msg(self):
        return "<TYPE>%s</TYPE><INFO>%s^%s</INFO>" % (
            self.msg_type, self.update_time, self.price)


class BidMessage(YayaMessage):

    """ 出价信息（抽象类） """

    msg_type = YayaMessageType.INFO_MSG
    info_re = re.compile(r'<INFO>(.*)</INFO>', re.IGNORECASE)

    def __init__(self, arg_list):
        self.arg_list = arg_list

    @classmethod
    def from_msg(cls, msg):
        info_groups = cls.info_re.search(msg)

        if info_groups:
            info = info_groups.group(1)
            info_list = info.split('^')
            return cls(info_list)

        return None


class BidTypeAMessage(BidMessage):

    """ 类型A出价信息 """

    info_re = re.compile(r'<INFO>A(.*)</INFO>', re.IGNORECASE)

    def to_msg(self):
        return "<TYPE>%s</TYPE><INFO>A%s</INFO>" % (
            self.msg_type, '^'.join(self.arg_list))


class BidTypeBMessage(BidMessage):

    """ 类型B出价信息 """

    info_re = re.compile(r'<INFO>B(.*)</INFO>', re.IGNORECASE)

    def to_msg(self):
        return "<TYPE>%s</TYPE><INFO>B%s</INFO>" % (
            self.msg_type, '^'.join(self.arg_list))


class BidTypeCMessage(BidMessage):

    """ 类型C出价信息 """

    info_re = re.compile(r'<INFO>C(.*)</INFO>', re.IGNORECASE)

    def to_msg(self):
        return "<TYPE>%s</TYPE><INFO>C%s</INFO>" % (
            self.msg_type, ''.join(self.arg_list))

class MyBidInfoMessage(YayaMessage):

    """ 由自身服务器返回的MyBidMessageInfo """

    mybidinfo_re = re.compile(r'<MYBIDINFO>(.*)</MYBIDINFO>', re.IGNORECASE)

    def __init__(self, update_time, price):
        self.update_time = update_time
        self.price = price

    @classmethod
    def from_msg(cls, msg):
        info_groups = cls.mybidinfo_re.search(msg)
        if info_groups:
            arg_list = info_groups.group(1).split('^')
            if len(arg_list):
                update_time = arg_list[0]
                price = arg_list[1]

                if TIME_RE.match(update_time) and INT_RE.match(price):
                    return cls(update_time, price)

        return None

    def to_msg(self):
        return '<MYBIDINFO>%s^%s</MYBIDINFO>' % (self.update_time, self.price)

MESSAGE_MAP = {
    YayaMessageType.CLIENT_MSG: [HelloClientMessage],
    YayaMessageType.FORMAT_MSG: [HelloMessage, FormatMessage],
    YayaMessageType.UPDATE_MSG: [UpdatePriceMessage],
    YayaMessageType.INFO_MSG: [BidTypeAMessage, BidTypeBMessage],
    None: [MyBidInfoMessage],
}
