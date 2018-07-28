# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(383, 283)
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setMargin(12)
        self.verticalLayout.setSpacing(16)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(MainWindow)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_machinecode = QtGui.QLineEdit(MainWindow)
        self.lineEdit_machinecode.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_machinecode.setReadOnly(False)
        self.lineEdit_machinecode.setObjectName(_fromUtf8("lineEdit_machinecode"))
        self.gridLayout.addWidget(self.lineEdit_machinecode, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(MainWindow)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.textEdit_activationcode = QtGui.QTextEdit(MainWindow)
        self.textEdit_activationcode.setReadOnly(True)
        self.textEdit_activationcode.setObjectName(_fromUtf8("textEdit_activationcode"))
        self.gridLayout.addWidget(self.textEdit_activationcode, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(MainWindow)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_usefullife = QtGui.QLineEdit(MainWindow)
        self.lineEdit_usefullife.setMinimumSize(QtCore.QSize(0, 25))
        self.lineEdit_usefullife.setObjectName(_fromUtf8("lineEdit_usefullife"))
        self.gridLayout.addWidget(self.lineEdit_usefullife, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_generator = QtGui.QPushButton(MainWindow)
        self.pushButton_generator.setObjectName(_fromUtf8("pushButton_generator"))
        self.horizontalLayout.addWidget(self.pushButton_generator)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_cancel = QtGui.QPushButton(MainWindow)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "软件授权", None))
        self.label.setText(_translate("MainWindow", "机器码", None))
        self.label_2.setText(_translate("MainWindow", "激活码", None))
        self.label_3.setText(_translate("MainWindow", "有效期", None))
        self.pushButton_generator.setText(_translate("MainWindow", "生成", None))
        self.pushButton_cancel.setText(_translate("MainWindow", "取消", None))

