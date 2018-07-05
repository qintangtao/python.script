#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PyQt4 import QtCore


class LoginThread(QtCore.QThread):

    signal_login = QtCore.pyqtSignal(bool)

    def __init__(self, dump, parent=None):
        super(LoginThread, self).__init__(parent)
        self.dump = dump

    def run(self):
        r = False
        if self.dump.request_account() or self.dump.request_login():
            r = True
        self.signal_login.emit(r)
