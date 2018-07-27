#!/usr/bin/python
# -*- coding: UTF-8 -*-
import res
import data
from PyQt4 import QtGui
from ui_mainwindow import Ui_MainWindow
from qin import softwarelicence


def gbk2utf8(txt):
    return unicode(txt, 'gbk').encode('utf-8')


def utf82gbk(txt):
    return unicode(txt, 'utf-8').encode('gbk')


def qstr2str(txt):
    return unicode(txt.toUtf8(), 'utf8', 'ignore')


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(':/bug.ico'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit_usefullife.setText('90')
        self.ui.pushButton_generator.clicked.connect(self.onGeneratorClicked)
        self.ui.pushButton_cancel.clicked.connect(self.onCancelClicked)
        softwarelicence.get_machinecode()

    def onGeneratorClicked(self):
        machinecode = qstr2str(self.ui.lineEdit_machinecode.text())
        usefullife = qstr2str(self.ui.lineEdit_usefullife.text())
        if machinecode == '' or usefullife == '':
            self.ui.textEdit_serialnumber.setText('')
            return
        serialnumber = softwarelicence.get_serialnumber(
            data.public_key, machinecode, int(usefullife))
        self.ui.textEdit_serialnumber.setText(serialnumber)

    def onCancelClicked(self):
        super(MainWindow, self).close()
