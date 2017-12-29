#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
import shutil

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
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def test_switch():
    v = 'ten'
    for case in switch(v):
        if case('one'):
            print 1
            break
        if case('two'):
            print 2
            break
        if case('ten'):
            print 10
            break
        if case('eleven'):
            print 11
            break
        if case():
            print "something else!"

CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET
def loggins_set_level(level):
    root=logging.getLogger()
    root.setLevel(level)

def logging_config():
    loggins_set_level(DEBUG)
    '''
    root=logging.getLogger()
    hdlr = logging.StreamHandler()
    root.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s %(filename)s(%(lineno)d) %(levelname)s %(message)s', '%Y:%m:%d %H:%M:%S')
    hdlr.setFormatter(fmt)
    root.addHandler(hdlr)
    '''
    
def test_loging():
    logging_config()
    logging.debug('This is debug message')
    logging.info('This is info message')
    logging.warning('This is warning message')

"""
save string to file

@param filepath: file path
@param model: open model
@param str: save text

@return: 0 - error, 1 - ok
"""
def save_file(filepath, model, str):
    of = open(filepath, model)
    if of:
        of.write(str)
        of.close()
        return 1
    else:
        return 0

def save_file_a(filepath, str):
    return save_file(filepath, "a", str)

def save_file_wb(filepath, str):
    return save_file(filepath, "wb", str)

def test_save_file():
    save_file_a("e://aa.arm", "asdfasdf")


def strf(msg, *args):
    if args: msg = msg % args
    return msg

def rmdirs(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

if __name__ == "__main__":
    print strf("0x%x %s", 123, "adsfads")
    msg="0x%x %s" % (123,"adsfads")
    print msg