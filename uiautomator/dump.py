#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

if os.path.exists('window_dump.xml'):
	os.remove('window_dump.xml')
if os.path.exists('window_dump.uix'):
	os.remove('window_dump.uix')
if os.path.exists('window_dump.png'):
	os.remove('window_dump.png')

print 'start window_dump.xml'
os.system('adb shell rm -rf /sdcard/window_dump.xml')
os.system('adb shell uiautomator dump /sdcard/window_dump.xml')
os.system('adb pull /sdcard/window_dump.xml')
if os.path.exists('window_dump.xml'):
	os.rename('window_dump.xml', 'window_dump.uix')
print 'done window_dump.xml'

print 'start window_dump.png'
os.system('adb shell rm -rf /sdcard/window_dump.png')
os.system('adb shell screencap /sdcard/window_dump.png')
os.system('adb pull /sdcard/window_dump.png')
print 'done window_dump.png'
