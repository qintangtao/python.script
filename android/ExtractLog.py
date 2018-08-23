#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys


def save_file(filename, data):
    try:
        with open(filename, 'w') as f:
            f.write(data)
            return True
    except Exception, e:
        print str(e)
    return False


def read_file(filename, tag, header):
    try:
        log = ''
        with open(filename, 'r') as f:
            for line in f:
                if line.find(tag) == 2:
                    idx = line.find(header, 2)
                    if idx > 2:
                        idx += len(header)
                        log += line[idx:].rstrip()
        if log != '':
            save_file(tag + '_' + header + '.log', log)
            print 'Success'
        else:
            print 'Failed'
    except Exception, e:
        print str(e)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        read_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print 'ExtractLog.py filname tag header'
        print 'ExtractLog.py qiyi.log byqin #1534993789310#'
