#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import logging
from qin import utils
from qin import rsa


def get_machinecode():
    return utils.get_md5(utils.machine_info())


def get_serialnumber(public_key, machine, usefullife):
    createdate = utils.millis_timestamp()
    finishdate = createdate + usefullife * 24 * 60 * 60 * 1000
    data = {'machine': machine, 'createdate': createdate,
            'finishdate': finishdate}
    return rsa.encrypt(public_key, json.dumps(data))


def verify_licence(private_key, licence):
    try:
        d = rsa.decrypt(private_key, licence)
        data = json.loads(d)
        if data['machine'] != get_machinecode():
            return False

        createdate = data['createdate']
        finishdate = data['finishdate']
        nowdate = utils.millis_timestamp()
        #print createdate, finishdate, nowdate
        if nowdate <= createdate or nowdate > finishdate:
            return False

        return True
    except Exception, e:
        logging.error(str(e))
        print str(e)
    return False


def verify_licencefile(private_key):
    licence = read_licence()
    if licence and len(licence) > 0:
        return verify_licence(private_key, licence)
    return False


def write_licence(data):
    filename = os.path.join(os.getcwd(), "software.licence")
    utils.save_file_w(filename, data)


def read_licence():
    filename = os.path.join(os.getcwd(), "software.licence")
    if os.path.exists(filename):
        return utils.read_file_r(filename)
    return None
