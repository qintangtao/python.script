#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import time
import logging
import platform
import hashlib
import requests
import json
import random
import zlib
import uuid
import wmi

if sys.version_info[0] == 2:
    def b(s):
        return s
    def bchr(s):
        return chr(s)
    def bstr(s):
        return str(s)
    def bord(s):
        return ord(s)
    if sys.version_info[1] == 1:
        def tobytes(s):
            try:
                return s.encode('latin-1')
            except:
                return ''.join(s)
    else:
        def tobytes(s):
            if isinstance(s, str):
                return s.encode("latin-1")
            else:
                return ''.join(s)
else:
    def b(s):
       return s.encode("latin-1") # utf-8 would cause some side-effects we don't want
    def bchr(s):
        return bytes([s])
    def bstr(s):
        if isinstance(s,str):
            return bytes(s,"latin-1")
        else:
            return bytes(s)
    def bord(s):
        return s
    def tobytes(s):
        if isinstance(s,bytes):
            return s
        else:
            if isinstance(s,str):
                return s.encode("latin-1")
            else:
                return bytes(s)

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
    filename = os.path.join(path, '%d%02d%02d.log' %
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
    return get_md5(uid)


def machine_info():
    uid = platform.platform()
    uid += '-'
    uid += platform.machine()
    uid += '-'
    uid += platform.node()
    uid += '-'
    uid += platform.processor()
    uid += '-'
    uid += get_mac()
    return uid


def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0, 11, 2)])


def get_md5(str):
    hash = hashlib.md5()
    hash.update(str.encode(encoding='utf-8'))
    return hash.hexdigest()


def get_sha1(str):
    hash = hashlib.sha1()
    hash.update(str.encode(encoding='utf-8'))
    return hash.hexdigest()


def get_crc32(str):
    return zlib.crc32(str)


def get_md5_file(filename):
    return get_md5(read_file_rb(filename))


def get_sha1_file(filename):
    return get_sha1(read_file_rb(filename))


def get_crc32_file(filename):
    return get_crc32(read_file_rb(filename))


def request_get(url, params=None, **kwargs):
    try:
        r = requests.get(url, params, **kwargs)
        if r.ok:
            logging.debug(r.content)
            return r.content
        else:
            r.raise_for_status()
    except Exception as e:
        logging.debug(str(e))
    return None


def request_post(url, data, **kwargs):
    try:
        r = requests.post(url, data, **kwargs)
        if r.ok:
            logging.debug(r.content)
            return r.content
        else:
            r.raise_for_status()
    except Exception as e:
        logging.debug(str(e))
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
    except Exception as e:
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
    except Exception as e:
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


def download_file(path, url, **args):
    basename = ''
    if 'basename' in args:
        basename = args['basename']
    if basename is None or basename == '':
        basename = os.path.basename(url)
    retry = False
    if 'retry' in args:
        retry = args['retry']
    filename = os.path.join(path, basename)
    if os.path.exists(filename):
        if retry:
            os.remove(filename)
        else:
            return True
    return request_file(filename, url)


def gmt_timestamp(gmt):
    return time.mktime(time.strptime(gmt, '%a, %d %b %Y %H:%M:%S GMT')) + (8 * 60 * 60)


def timestamp_datetime(tm):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tm))


def datetime_timestamp(dt):
    return time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))


def millis_timestamp(t=time.time()):
    msTime = lambda: int(round(t * 1000))
    return msTime()


def request_nowtime():
    try:
        r = requests.get('http://www.beijing-time.org/')
        if r.ok:
            logging.debug(r.headers)
            tm = gmt_timestamp(r.headers['Date'])
            return millis_timestamp(tm)
        else:
            logging.error('r is not ok')
    except Exception as e:
        logging.error(str(e))
    return 0


def is_overdue(timestamp):
    nowtime = request_nowtime()
    if nowtime > timestamp:
        return True
    return False


def random_check(a=1, b=100, c=2):
    random.seed()
    r = random.randint(a, b)
    if r % c == 0:
        return True
    return False

class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


def test_switch():
    v = 'ten'
    for case in switch(v):
        if case('one'):
            print (1)
            break
        if case('two'):
            print (2)
            break
        if case('ten'):
            print (10)
            break
        if case('eleven'):
            print (11)
            break
        if case():
            print ("something else!" )  

def test_switch2():
    v = 10
    for case in switch(v):
        if case(1):
            print (1)
            break
        if case(2):
            print (2)
            break
        if case(10):
            print (10)
            break
        if case(11):
            print (11)
            break
        if case():
            print ("something else!" )               

if __name__ == "__main__":
    hardware_str = ""
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        print ('cpu.LoadPercentage:', cpu.LoadPercentage)
        print ('cpu.ProcessorId:', cpu.ProcessorId.strip())
        hardware_str += cpu.ProcessorId.strip()
        hardware_str += ';'
    for disk in c.Win32_DiskDrive():
        print ('disk.SerialNumber:', disk.SerialNumber.strip())
        print ('disk.Caption:', disk.Caption)
        print ('disk.Size:', int(disk.Size)/1000/1000/1000)
        hardware_str += disk.SerialNumber.strip()
        hardware_str += ';'
    for board in c.Win32_BaseBoard():
        print ('board.SerialNumber:', board.SerialNumber.strip())
        hardware_str += board.SerialNumber.strip()
        hardware_str += ';'
    for mac in c.Win32_NetworkAdapter():
        print ('mac.MACAddress:', mac.MACAddress)
    for bios in c.Win32_BIOS():
        print ('bios.SerialNumber:', bios.SerialNumber.strip())
        hardware_str += bios.SerialNumber.strip()
        hardware_str += ';'

    print ('hardware_str:', hardware_str)

    for my_computer in c.Win32_ComputerSystem():
        print (("Disks on", my_computer.Name))
    for disk in c.Win32_LogicalDisk():
        print ((disk.Caption, disk.Description, disk.ProviderName or ""))
    for disk in c.Win32_LogicalDisk():
        if disk.DriveType == 3:
            space = 100 * int(disk.FreeSpace) / int(disk.Size)
            print ("%s has %d%% free" % (disk.Name, space))

    test_switch2()
    
    '''
    print random_check()
    if is_overdue(123):
        print 'True'
    else:
        print 'False'
    '''
