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
        MainWindow.resize(704, 484)
        MainWindow.setStyleSheet(_fromUtf8("QGroupBox{\n"
"font-weight:bold;\n"
"}\n"
"QScrollBar:vertical{\n"
"width:6px;\n"
"max-width:6px;\n"
"background:rgb(255,255,255);\n"
"padding:0px;\n"
"}\n"
"QScrollBar::add-page:vertical,\n"
"QScrollBar::sub-page:vertical{\n"
"background:rgba(0,0,0,0%);\n"
"}\n"
"QScrollBar::handle:vertical{\n"
"background:rgba(0,0,0,25%);\n"
"border-radius:3px;\n"
"min-height:30px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{\n"
"background:rgba(0,0,0,50%);\n"
"}\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical{\n"
"height:0px;\n"
"}\n"
"QTableView{\n"
"border: 1 solid #D8D8D8;\n"
"}"))
        self.verticalLayout = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_settings = QtGui.QGroupBox(MainWindow)
        self.groupBox_settings.setObjectName(_fromUtf8("groupBox_settings"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_settings)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_gender = QtGui.QLabel(self.groupBox_settings)
        self.label_gender.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gender.setObjectName(_fromUtf8("label_gender"))
        self.horizontalLayout.addWidget(self.label_gender)
        self.comboBox_gender = QtGui.QComboBox(self.groupBox_settings)
        self.comboBox_gender.setObjectName(_fromUtf8("comboBox_gender"))
        self.horizontalLayout.addWidget(self.comboBox_gender)
        self.label_major = QtGui.QLabel(self.groupBox_settings)
        self.label_major.setAlignment(QtCore.Qt.AlignCenter)
        self.label_major.setObjectName(_fromUtf8("label_major"))
        self.horizontalLayout.addWidget(self.label_major)
        self.comboBox_major = QtGui.QComboBox(self.groupBox_settings)
        self.comboBox_major.setObjectName(_fromUtf8("comboBox_major"))
        self.horizontalLayout.addWidget(self.comboBox_major)
        self.label_minor = QtGui.QLabel(self.groupBox_settings)
        self.label_minor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_minor.setObjectName(_fromUtf8("label_minor"))
        self.horizontalLayout.addWidget(self.label_minor)
        self.comboBox_minor = QtGui.QComboBox(self.groupBox_settings)
        self.comboBox_minor.setObjectName(_fromUtf8("comboBox_minor"))
        self.horizontalLayout.addWidget(self.comboBox_minor)
        self.label_status = QtGui.QLabel(self.groupBox_settings)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.horizontalLayout.addWidget(self.label_status)
        self.comboBox_status = QtGui.QComboBox(self.groupBox_settings)
        self.comboBox_status.setObjectName(_fromUtf8("comboBox_status"))
        self.horizontalLayout.addWidget(self.comboBox_status)
        self.label_sort = QtGui.QLabel(self.groupBox_settings)
        self.label_sort.setObjectName(_fromUtf8("label_sort"))
        self.horizontalLayout.addWidget(self.label_sort)
        self.comboBox_sort = QtGui.QComboBox(self.groupBox_settings)
        self.comboBox_sort.setObjectName(_fromUtf8("comboBox_sort"))
        self.horizontalLayout.addWidget(self.comboBox_sort)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)
        self.horizontalLayout.setStretch(3, 3)
        self.horizontalLayout.setStretch(4, 1)
        self.horizontalLayout.setStretch(5, 3)
        self.horizontalLayout.setStretch(6, 1)
        self.horizontalLayout.setStretch(7, 3)
        self.horizontalLayout.setStretch(8, 1)
        self.horizontalLayout.setStretch(9, 3)
        self.verticalLayout.addWidget(self.groupBox_settings)
        self.groupBox_dump = QtGui.QGroupBox(MainWindow)
        self.groupBox_dump.setObjectName(_fromUtf8("groupBox_dump"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_dump)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_before_page = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_before_page.setMinimumSize(QtCore.QSize(40, 0))
        self.pushButton_before_page.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_before_page.setObjectName(_fromUtf8("pushButton_before_page"))
        self.horizontalLayout_2.addWidget(self.pushButton_before_page)
        self.lineEdit_page_index = QtGui.QLineEdit(self.groupBox_dump)
        self.lineEdit_page_index.setMinimumSize(QtCore.QSize(35, 0))
        self.lineEdit_page_index.setMaximumSize(QtCore.QSize(35, 16777215))
        self.lineEdit_page_index.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_page_index.setObjectName(_fromUtf8("lineEdit_page_index"))
        self.horizontalLayout_2.addWidget(self.lineEdit_page_index)
        self.label_page_limit = QtGui.QLabel(self.groupBox_dump)
        self.label_page_limit.setMaximumSize(QtCore.QSize(5, 16777215))
        self.label_page_limit.setObjectName(_fromUtf8("label_page_limit"))
        self.horizontalLayout_2.addWidget(self.label_page_limit)
        self.lineEdit_page_total = QtGui.QLineEdit(self.groupBox_dump)
        self.lineEdit_page_total.setMinimumSize(QtCore.QSize(35, 0))
        self.lineEdit_page_total.setMaximumSize(QtCore.QSize(35, 16777215))
        self.lineEdit_page_total.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_page_total.setReadOnly(True)
        self.lineEdit_page_total.setObjectName(_fromUtf8("lineEdit_page_total"))
        self.horizontalLayout_2.addWidget(self.lineEdit_page_total)
        self.pushButton_after_page = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_after_page.setMinimumSize(QtCore.QSize(40, 0))
        self.pushButton_after_page.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_after_page.setObjectName(_fromUtf8("pushButton_after_page"))
        self.horizontalLayout_2.addWidget(self.pushButton_after_page)
        self.pushButton_refresh = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout_2.addWidget(self.pushButton_refresh)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_remove = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_remove.setObjectName(_fromUtf8("pushButton_remove"))
        self.horizontalLayout_2.addWidget(self.pushButton_remove)
        self.pushButton_sources = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_sources.setObjectName(_fromUtf8("pushButton_sources"))
        self.horizontalLayout_2.addWidget(self.pushButton_sources)
        self.pushButton_start = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.horizontalLayout_2.addWidget(self.pushButton_start)
        self.pushButton_stop = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_stop.setObjectName(_fromUtf8("pushButton_stop"))
        self.horizontalLayout_2.addWidget(self.pushButton_stop)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tableView = QtGui.QTableView(self.groupBox_dump)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)
        self.verticalLayout.addWidget(self.groupBox_dump)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "免费小说书城 by Qin", None))
        self.groupBox_settings.setTitle(_translate("MainWindow", "设置", None))
        self.label_gender.setText(_translate("MainWindow", "性别", None))
        self.label_major.setText(_translate("MainWindow", "主类", None))
        self.label_minor.setText(_translate("MainWindow", "次类", None))
        self.label_status.setText(_translate("MainWindow", "状态", None))
        self.label_sort.setText(_translate("MainWindow", "排序", None))
        self.groupBox_dump.setTitle(_translate("MainWindow", "转存", None))
        self.pushButton_before_page.setText(_translate("MainWindow", "<<", None))
        self.label_page_limit.setText(_translate("MainWindow", "/", None))
        self.pushButton_after_page.setText(_translate("MainWindow", ">>", None))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新", None))
        self.pushButton_remove.setText(_translate("MainWindow", "删除", None))
        self.pushButton_sources.setText(_translate("MainWindow", "书源", None))
        self.pushButton_start.setText(_translate("MainWindow", "开始", None))
        self.pushButton_stop.setText(_translate("MainWindow", "停止", None))

