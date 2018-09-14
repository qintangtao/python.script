#!/usr/bin/python
# -*- coding: UTF-8 -*-
import frida
import sys

jscode = """
if(Java.available) {
	Java.perform(function(){
		var a = Java.use("com.youku.upsplayer.module.VideoInfo");
		if(a != undefined) {
			console.log("VideoInfo: " + a.toString());
		} else {
			console.log("VideoInfo: undefined");
		}
	})
}
"""

jscode2 = """
	send(11111);
	if(Java.available) {
		console.log("Java.available is True");
		Java.perform(function(){
			console.log("Java.perform is True");
		});
	} else {
		console.log("Java.available is False");
	}
	send(2222222);
"""

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


def frida_hook():
    rdev = frida.get_device_manager().enumerate_devices()[-1]
    print rdev
    pid = rdev.spawn(['com.youku.phone'])
    print pid
    session = rdev.attach(pid)
    print('[*] Attach Application id:', pid)
    rdev.resume(pid)
    print('[*] Application onResume')
    script = session.create_script(jscode)
    script.on('message', on_message())
    print('[*] Running CTF')
    script.load()
    sys.stdin.read()


def frida_hook2():
    rdev = frida.get_usb_device()
    print rdev
    pid = rdev.spawn(['com.youku.phone'])
    print pid
    session = rdev.attach(pid)
    #session = rdev.attach("com.youku.phone")
    print session
    script = session.create_script(jscode)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()


def frida_hook3():
    rdev = frida.get_usb_device()
    print rdev
    pid = rdev.spawn(['com.youku.phone'])
    print pid
    session = rdev.attach(pid)
    #session = rdev.attach("com.youku.phone")
    print session
    script = session.create_script(jscode2)
    script.on('message', on_message)
    script.load()
    sys.stdin.read()

# test_frida()
frida_hook3()

# frida_hook()
