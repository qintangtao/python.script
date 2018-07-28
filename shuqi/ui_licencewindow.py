# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'licencewindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LicenceWindow(object):
    def setupUi(self, LicenceWindow):
        LicenceWindow.setObjectName(_fromUtf8("LicenceWindow"))
        LicenceWindow.resize(346, 232)
        self.verticalLayout = QtGui.QVBoxLayout(LicenceWindow)
        self.verticalLayout.setMargin(12)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(LicenceWindow)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_machinecode = QtGui.QLineEdit(LicenceWindow)
        self.lineEdit_machinecode.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_machinecode.setReadOnly(True)
        self.lineEdit_machinecode.setObjectName(_fromUtf8("lineEdit_machinecode"))
        self.gridLayout.addWidget(self.lineEdit_machinecode, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(LicenceWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.textEdit_activationcode = QtGui.QTextEdit(LicenceWindow)
        self.textEdit_activationcode.setObjectName(_fromUtf8("textEdit_activationcode"))
        self.gridLayout.addWidget(self.textEdit_activationcode, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_register = QtGui.QPushButton(LicenceWindow)
        self.pushButton_register.setObjectName(_fromUtf8("pushButton_register"))
        self.horizontalLayout.addWidget(self.pushButton_register)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_cancel = QtGui.QPushButton(LicenceWindow)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(LicenceWindow)
        QtCore.QMetaObject.connectSlotsByName(LicenceWindow)

    def retranslateUi(self, LicenceWindow):
        LicenceWindow.setWindowTitle(_translate("LicenceWindow", "软件授权", None))
        self.label.setText(_translate("LicenceWindow", "机器码", None))
        self.label_2.setText(_translate("LicenceWindow", "激活码", None))
        self.pushButton_register.setText(_translate("LicenceWindow", "注册", None))
        self.pushButton_cancel.setText(_translate("LicenceWindow", "取消", None))

