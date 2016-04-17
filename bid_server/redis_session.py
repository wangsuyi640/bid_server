# *_* coding=utf8 *_*
#!/usr/bin/env python

try:
    import cPickle as pickle
except ImportError:
    import pickle
import time
import logging
from uuid import uuid4

class RedisSessionStore(object):
    def __init__(self, redis_connection, **options):
        self.options = {
            'key_prefix': 'bid.server.session',
            'expire': 7200,
        }
        self.options.update(options)
        self.redis = redis_connection

    def prefixed(self, sid):
        return '%s:%s' % (self.options['key_prefix'], sid)

    def generate_sid(self):
        return uuid4().get_hex()

    def get_session(self, sid, name):
        data = self.redis.hget(self.prefixed(sid), name)
        session = pickle.loads(data) if data else dict()
        return session

    def set_session(self, sid, session_data, name, expire=None):

        self.redis.hset(self.prefixed(sid), name, pickle.dumps(session_data))
        expire = expire or self.options['expire']
        if expire:
            self.redis.expire(self.prefixed(sid), expire)

    def delete_session(self, sid):
        return self.redis.delete(self.prefixed(sid))


class RedisSession(object):
    def __init__(self, session_store, session_id=None, expires_days=None):
        self._store = session_store
        self._sid = session_id if session_id else self._store.generate_sid()
        self._dirty = False
        self.set_expires(expires_days)
        
        try:
            self._data = self._store.get_session(self._sid, 'data')
        except:
            logging.error('Can not connect Redis server.')
            self._data = {}


    def clear(self):
        self._store.delete_session(self._sid)

    @property
    def id(self):
        return self._sid
    
    def access(self, remote_ip):
        access_info = {'remote_ip':remote_ip, 'time':'%.6f' % time.time()}
        self._store.set_session(
                self._sid,
                'last_access',
                pickle.dumps(access_info))

    def last_access(self):
        access_info = self._store.get_session(self._sid, 'last_access')
        return pickle.loads(access_info)

    def set_expires(self, days):
        self._expiry = days * 86400 if days else None

    def get(self, key):
        return self._data.get(key)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._dirty = True

    def __delitem__(self, key):
        del self._data[key]
        self._dirty = True

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):
        return key in self._data

    def __iter__(self):
        for key in self._data:
            yield key

    def __repr__(self):
        return self._data.__repr__()

    
    def __del__(self):
        if self._dirty:
            self.save()

    def save(self):
        self._store.set_session(self._sid, self._data, 'data', self._expiry)
        self._dirty = False