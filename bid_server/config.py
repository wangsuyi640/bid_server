# *_* coding=utf8 *_*
#!/usr/bin/env python

import os

# 当前的调试状态
IS_DEBUG = True
ROOT_PATH = os.path.dirname(__file__)

# ------------------ SQLALCHEMY CONFIG -----------------------

SQLITE_PATH = ROOT_PATH
DB_CONNECTION = "sqlite:////%s/bid.sqlite" % ROOT_PATH
MAX_DB_RETRY_TIMES = 10
SQL_RETRY_INTERVAL = 1
SQL_IDLE_TIMEOUT = 1

SESSION_PERMAMENT_DAYS = 3
SESSION_REDIS_HOST = "127.0.0.1"
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0

# -------------------- UDP secondary server ------------------

# UDP服务端监听端口号
UDP_PORT = 990
# 客户端会话过期时间
SESSION_EXPIRE_SECONDS = 60


# -------------------- RPC server ------------------------------
RPC_PORT = 22222

# -------------------- Business 业务逻辑部分 ---------------------

BUSINESS_PORT = 8080
ADMIN_INIT_PASSWORD = "admin"

# Config Pubkey
CONFIG_PUBKEY = """
-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAzHH2QWRUHoPIxgLi7q7uEWlWwmhUf7SMn0+Y0fAuQRM4/F+48ABL
d+vSf0WGQ3bJVqIDS6ROqtLLLJgfQ0DyRumaprAAqBPaSesM1M/HTqfmBMXQBLIY
XADI2pVwcCPY2OUkqf4fDqBOanJn4G8ejWgxMiSUEgeqaDdc0dZ7CgGMljnGihJ8
PVxdCWeChpOEV6YKgKp1r4SBPmNYxTcNvVWDPPmyQZdluBOEdTrcQxGWYF2pQPlH
hxFvVLKctu+VIfmCQi9Numxi+RofD5HE/2pX/H7tuwubmJljfDRql0tYN8xB/H7j
Oh0/t6e531E9SHtZmax/sF5PZztVzIRrOQIDAQAB
-----END RSA PUBLIC KEY-----
"""
# Config Privvate key
CONFIG_PRIVKEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEqgIBAAKCAQEAzHH2QWRUHoPIxgLi7q7uEWlWwmhUf7SMn0+Y0fAuQRM4/F+4
8ABLd+vSf0WGQ3bJVqIDS6ROqtLLLJgfQ0DyRumaprAAqBPaSesM1M/HTqfmBMXQ
BLIYXADI2pVwcCPY2OUkqf4fDqBOanJn4G8ejWgxMiSUEgeqaDdc0dZ7CgGMljnG
ihJ8PVxdCWeChpOEV6YKgKp1r4SBPmNYxTcNvVWDPPmyQZdluBOEdTrcQxGWYF2p
QPlHhxFvVLKctu+VIfmCQi9Numxi+RofD5HE/2pX/H7tuwubmJljfDRql0tYN8xB
/H7jOh0/t6e531E9SHtZmax/sF5PZztVzIRrOQIDAQABAoIBAQCybAa43QFYvDQ9
MwmvunTEN0VjVr/fz8clxcad+Vm0qz0Ba9yvf+JdHy7OqfNZ71IZTD1KB3QsOtjb
60rlW8nVP0wbiuCXzvOjrQG+vDK5n2fr5GL9phwCNyETOnYtN+uoppoPzVp3Xknx
NjUXtoJYcIT2uNuMvKktbl/pdIVvrVh8TB/3TjAQEVT+4I7lDpjrcQUWOwf0YT7o
guMkRrUSdy7yOEyuQtLM+JoZibUZuCrpoGFkJWdTtcPRg5Lr4Zm8GtKJWH64RZxq
8JX7hR2R5RNP8aMLFqL4dqgbkmj9rGezWdo8WjphBteGAzhbKpWEZ1jGWomhHjIg
f50KOqVNAoGJANYscbyEX/oQVjzEbeV5ZNbWQ72TTL0XvNXGpOZTw/OvoxD1O15c
GVD22h3iXtFD/DTR7QCrfq3PlZv7e3nxBgrbjkQChtUZn6n6TdrxcFNA6+vnJZ2Z
i8DtlmpcgBsCikitGtmKXZa7VMg7FKeHwqBN6ZOdLj3qVvFfO0jtZaxlyOOyiTIb
EKsCeQD0XyV7NkbSBFNtJG2OfFj+UpDXVO3jznwUPyb/u9wALFv0tDr4Ios2cX+a
84Vk1DyNt3XWWR8vUDOLUgPjvfOoiXVijuZn2RsZDLnRdFlkusmu2EHv+bqA9ZDn
3S5GAM2CneiEYxzdqkYGn9BfEQLyVGX6AZOK26sCgYgrHvmrVg+o3l8ujvH9cMqP
wsYSxjR+IehgNkV/JkBesO8o++b/IZXrSjgyKiCjC4gc7mNEbkLsJc5egGyk6ZUo
3HmxUbzp7OXLqFzChzfxWzHk5j4ZlA+iQXO2aHdWeNV0un2cbRJYxdDVG6gV7uyN
sAImOVBVIPhuUpkyHrII2tlulsSutOpPAnkAyBe4OwEgUArWvMFdK5RJ0kSM8KRL
/YIvOuzS5AdQhpvL17xTpKW0U6nvkFLh4MOfqXKU/CQRUs5axjMrmCkK/+89vKvB
oTq143b2F7krET2Ysp/ErdhPjBSGyDPlFdDGdbMSloQJOL+ZgwcMuSrWvNG6hlEQ
HFztAoGIeA8mmrulC2X04Vhy5qx94eziW1pjMe2IUkjCZeldWjwyYNsHVAOtF7QB
LQlkpeF4pI2ChaEPukcfQC6PrKH1U06Y4UUfQKLF6LTeYX/YlXAQ18+/v5zrhz9H
Dna2CAQzNKICKs+BELUU9J52JTb2RqoCXKtNQK4XRlHl4eN6KbdrSVnQitwt9A==
-----END RSA PRIVATE KEY-----
"""


# -------------------- Mock Web server 业务逻辑部分 ------------------

MOCK_WEB_PORT = 80
MOCK_UDP_PORT = 999
