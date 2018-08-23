#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import re


def save_file(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write(data)
            return True
    except Exception, e:
        print str(e)
    return False


def read_file(filename):
    try:
        log = ''
        tag = ''
        block = ''
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    #I/byqin   (16146): #1534993799118#
                    list_item = re.findall(
                        r'(\w{1}/\w+\s+\(\d+\):\s+)(#\d+#)', line)
                    if len(list_item) == 1:
                        item = list_item[0]
                        if tag != item[1]:
                            if block.strip():
                                log += block
                                log += '\r\n'
                            tag = item[1]
                            block = item[0]
                        block += re.sub(re.compile(
                            r'(\w{1}/\w+\s+\(\d+\):\s+)(#\d+#)'), '', line)
                    else:
                        log += line
                        log += '\r\n'
        if log != '':
            save_file(filename + '.log', log)
            print 'Success'
        else:
            print 'Failed'
    except Exception, e:
        print str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        read_file(sys.argv[1])
    else:
        print 'ExtractLog.py filname'
        print 'ExtractLog.py qiyi.log'
