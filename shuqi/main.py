#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import logging
import data
from PyQt4 import QtGui
from mainwindow import MainWindow
from licencewindow import LicenceWindow
from qin import softwarelicence
from qin import utils

reload(sys)
sys.setdefaultencoding('utf-8')


def AppInstance():
    try:
        global s
        s = socket.socket()
        s.bind((socket.gethostname(), 60123))
    except:
        print "instance is running..."
        sys.exit(1)


def main():
    utils.logging_config(os.getcwd(), logging.INFO)
    AppInstance()
    app = QtGui.QApplication(sys.argv)
    if softwarelicence.verify_licencefile(data.private_key) is False:
        w = LicenceWindow()
        w.show()
        if app.exec_() == 0:
            sys.exit(1)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
