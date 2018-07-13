#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import platform
import hashlib
import requests
import json

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
