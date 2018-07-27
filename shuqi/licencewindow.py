#!/usr/bin/python
# -*- coding: UTF-8 -*-
import res
import data
from PyQt4 import QtCore, QtGui
from ui_licencewindow import Ui_LicenceWindow
from qin import softwarelicence


def gbk2utf8(txt):
    return unicode(txt, 'gbk').encode('utf-8')


def utf82gbk(txt):
    return unicode(txt, 'utf-8').encode('gbk')


def qstr2str(txt):
    return unicode(txt.toUtf8(), 'utf8', 'ignore')


class LicenceWindow(QtGui.QWidget):

    def __init__(self):
        super(LicenceWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(':/bug.ico'))
        self.ui = Ui_LicenceWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit_machinecode.setText(softwarelicence.get_machinecode())
        self.ui.textEdit_serialnumber.setText(u"请把机器码发给管理员获取授权序列号")
        self.ui.pushButton_register.clicked.connect(self.onRegisterClicked)
        self.ui.pushButton_cancel.clicked.connect(self.onCancelClicked)

    def onRegisterClicked(self):
        serialnumber = qstr2str(self.ui.textEdit_serialnumber.toPlainText())
        if serialnumber == '':
            self.ui.textEdit_serialnumber.setText('')
            return
        if softwarelicence.verify_licence(data.private_key, serialnumber):
            softwarelicence.write_licence(serialnumber)
            QtGui.QMessageBox.information(self, u"软件授权", u"注册成功!")
            QtGui.qApp.exit(1)
        else:
            QtGui.QMessageBox.critical(
                self, u"软件授权", u"错误的序列号!", QtGui.QMessageBox.Ok)

    def onCancelClicked(self):
        super(LicenceWindow, self).close()
