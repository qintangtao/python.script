#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import logging
import wmi
import time
#from qin import utils
#from qin import rsa
import utils
import rsa

def get_machinecode():
    hardware_str = ""
    c = wmi.WMI()
    for cpu in c.Win32_Processor():
        hardware_str += cpu.ProcessorId.strip()
        hardware_str += ';'
    for disk in c.Win32_DiskDrive():
        hardware_str += disk.SerialNumber.strip()
        hardware_str += ';'
    for board in c.Win32_BaseBoard():
        hardware_str += board.SerialNumber.strip()
        hardware_str += ';'
    '''
    for mac in c.Win32_NetworkAdapter():
        print mac.MACAddress
    for bios in c.Win32_BIOS():
        print bios.SerialNumber.strip()
        hardware_str += bios.SerialNumber.strip()
        hardware_str += ';'
    '''
    logging.debug(hardware_str)
    return utils.get_md5(hardware_str)


def get_activationcode(public_key, machine, usefullife):
    createdate = utils.millis_timestamp()
    finishdate = createdate + usefullife * 24 * 60 * 60 * 1000
    data = {'machine': machine, 'createdate': createdate,
            'finishdate': finishdate}
    return rsa.encrypt(public_key, json.dumps(data).encode("utf-8")).decode("utf-8")


def verify_licence(private_key, licence):
    try:
        d = rsa.decrypt(private_key, licence).decode("utf-8")
        data = json.loads(d)
        logging.debug(data)
        print(data)
        if data['machine'] != get_machinecode():
            logging.info('machine: [%s],  [%s]', data[
                'machine'], get_machinecode())
            return False

        createdate = data['createdate']
        finishdate = data['finishdate']
        nowdate = utils.request_nowtime()

        if nowdate <= createdate or nowdate > finishdate:
            logging.info(
                'createdate[%d],  finishdate[%d],  nowdate[%d]', createdate, finishdate, nowdate)
            return False

        return True
    except Exception as e:
        logging.error(str(e))
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

if __name__ == "__main__":
    #utils.logging_config(os.getcwd(), logging.DEBUG)

    key = rsa.generator()

    machinecode = get_machinecode()
    print(machinecode)
   
    licence = get_activationcode(key[1], machinecode, 30)
    print(licence)

    write_licence(licence)

    time.sleep( 5 )

    verifylicence = verify_licence(key[0], licence)
    print(verifylicence)

    time.sleep( 2 )

    verifylicence = verify_licencefile(key[0])
    print(verifylicence)