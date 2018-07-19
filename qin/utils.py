#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import platform
import hashlib
import requests
import json
import random

'''
logging.CRITICAL
logging.FATAL
logging.ERROR
logging.WARNING
logging.WARN
logging.INFO
logging.DEBUG
logging.NOTSET
'''


def logging_config(path, level):
    t = time.localtime(time.time())
    path = os.path.join(path, 'log')
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, 'dump_%d%02d%02d.log' %
                            (t.tm_year, t.tm_mon, t.tm_mday))
    logging.basicConfig(level=level,
                        format='{%(funcName)s:%(lineno)d} <%(levelname)s> %(message)s',
                        filename=filename,
                        filemode='a')
    logging.getLogger("requests").setLevel(logging.CRITICAL)


def generate_uid():
    uid = platform.platform()
    uid += '-'
    uid += platform.machine()
    uid += '-'
    uid += platform.node()
    uid += '-'
    uid += platform.processor()
    return md5_str(uid)


def md5_str(str):
    hash = hashlib.md5()
    hash.update(str.encode(encoding='utf-8'))
    return hash.hexdigest()


def request_get(url, params=None, **kwargs):
    try:
        r = requests.get(url, params, **kwargs)
        if r.ok:
            logging.debug(r.content)
            return r.content
        else:
            r.raise_for_status()
    except Exception, e:
        logging.error(str(e))
    return None


def request_post(url, data, **kwargs):
    try:
        r = requests.get(url, data, **kwargs)
        if r.ok:
            logging.debug(r.content)
            return r.content
        else:
            r.raise_for_status()
    except Exception, e:
        logging.error(str(e))
    return None


def request_json_get(url, params=None, timeout=3, **kwargs):
    content = request_get(url, params, timeout=timeout, **kwargs)
    if content is None:
        return None
    return json.loads(content)


def request_json_post(url, data, timeout=3, **kwargs):
    content = request_post(url, data, timeout=timeout, **kwargs)
    if content is None:
        return None
    return json.loads(content)


def save_file(filename, mode, data):
    try:
        with open(filename, mode) as f:
            f.write(data)
            return True
    except Exception, e:
        logging.error(str(e))
    return False


def save_file_w(filename, data):
    return save_file(filename, 'w', data)


def save_file_wb(filename, data):
    return save_file(filename, 'wb', data)


def save_json(filename, dict):
    return save_file_w(filename, json.dumps(dict))


def read_file(filename, mode):
    try:
        with open(filename, mode) as f:
            return f.read()
    except Exception, e:
        logging.error(str(e))
    return None


def read_file_r(filename):
    return read_file(filename, 'r')


def read_file_rb(filename):
    return read_file(filename, 'rb')


def request_file(filename, url):
    content = request_get(url)
    if content is None:
        return False
    return save_file_wb(filename, content)


def download_file(path, url):
    filename = os.path.join(path, os.path.basename(url))
    if os.path.exists(filename):
        return True
    return request_file(filename, url)


def gmt_timestamp(gmt):
    return time.mktime(time.strptime(gmt, '%a, %d %b %Y %H:%M:%S GMT')) + (8 * 60 * 60)


def timestamp_datetime(tm):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tm))


def datetime_timestamp(dt):
    return time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))


def millis_timestamp(t):
    msTime = lambda: int(round(t * 1000))
    return msTime()


def is_overdue(timestamp):
    try:
        r = requests.get('http://www.beijing-time.org/')
        if r.ok:
            tm = gmt_timestamp(r.headers['Date'])
            mstm = millis_timestamp(tm)
            # print tm, mstm, timestamp
            if mstm > timestamp:
                return True
        else:
            print 'r is not ok'
    except Exception, e:
        print str(e)
    return False


def random_check():
    random.seed()
    r = random.randint(1, 100)
    if r % 2 == 0:
        return True
    return False

if __name__ == "__main__":
    print random_check()
    '''
    if is_overdue(123):
        print 'True'
    else:
        print 'False'
    '''
