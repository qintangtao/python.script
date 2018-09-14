#!/usr/bin/python
# -*- coding: UTF-8 -*-
import frida
import sys


def read_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception, e:
        print str(e)
    return None


def test_frida():
    rdev = frida.get_remote_device()
    print rdev
    front_app = rdev.get_frontmost_application()
    print front_app
    processes = rdev.enumerate_processes()
    for process in processes:
        print process


def on_message(message, data):
    if message['type'] == 'send':
        print message['payload']
    else:
        print message


def frida_hook(clazz, jscode):
    rdev = frida.get_usb_device()
    print rdev
    pid = rdev.spawn([clazz])
    print pid
    session = rdev.attach(pid)
    print session
    rdev.resume(pid)
    script = session.create_script(jscode)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()


def frida_hook2(clazz, jscode):
    rdev = frida.get_usb_device()
    print rdev
    session = rdev.attach(clazz)
    print session
    script = session.create_script(jscode)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()

if __name__ == '__main__':
    jscode = read_file('frida_code.js')
    if jscode is not None:
        frida_hook('com.youku.phone', jscode)
