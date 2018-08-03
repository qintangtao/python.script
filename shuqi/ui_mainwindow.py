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
        MainWindow.resize(777, 528)
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
        self.groupBox_settings.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox_settings.setObjectName(_fromUtf8("groupBox_settings"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_settings)
        self.horizontalLayout.setContentsMargins(9, 3, 9, 9)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.groupBox_settings)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_type = QtGui.QWidget()
        self.tab_type.setObjectName(_fromUtf8("tab_type"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab_type)
        self.horizontalLayout_4.setContentsMargins(0, 0, 6, 0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_gender = QtGui.QLabel(self.tab_type)
        self.label_gender.setAlignment(QtCore.Qt.AlignCenter)
        self.label_gender.setObjectName(_fromUtf8("label_gender"))
        self.horizontalLayout_4.addWidget(self.label_gender)
        self.comboBox_gender = QtGui.QComboBox(self.tab_type)
        self.comboBox_gender.setObjectName(_fromUtf8("comboBox_gender"))
        self.horizontalLayout_4.addWidget(self.comboBox_gender)
        self.label_major = QtGui.QLabel(self.tab_type)
        self.label_major.setAlignment(QtCore.Qt.AlignCenter)
        self.label_major.setObjectName(_fromUtf8("label_major"))
        self.horizontalLayout_4.addWidget(self.label_major)
        self.comboBox_major = QtGui.QComboBox(self.tab_type)
        self.comboBox_major.setObjectName(_fromUtf8("comboBox_major"))
        self.horizontalLayout_4.addWidget(self.comboBox_major)
        self.label_minor = QtGui.QLabel(self.tab_type)
        self.label_minor.setAlignment(QtCore.Qt.AlignCenter)
        self.label_minor.setObjectName(_fromUtf8("label_minor"))
        self.horizontalLayout_4.addWidget(self.label_minor)
        self.comboBox_minor = QtGui.QComboBox(self.tab_type)
        self.comboBox_minor.setObjectName(_fromUtf8("comboBox_minor"))
        self.horizontalLayout_4.addWidget(self.comboBox_minor)
        self.label_status = QtGui.QLabel(self.tab_type)
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName(_fromUtf8("label_status"))
        self.horizontalLayout_4.addWidget(self.label_status)
        self.comboBox_status = QtGui.QComboBox(self.tab_type)
        self.comboBox_status.setObjectName(_fromUtf8("comboBox_status"))
        self.horizontalLayout_4.addWidget(self.comboBox_status)
        self.label_sort = QtGui.QLabel(self.tab_type)
        self.label_sort.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sort.setObjectName(_fromUtf8("label_sort"))
        self.horizontalLayout_4.addWidget(self.label_sort)
        self.comboBox_sort = QtGui.QComboBox(self.tab_type)
        self.comboBox_sort.setObjectName(_fromUtf8("comboBox_sort"))
        self.horizontalLayout_4.addWidget(self.comboBox_sort)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 3)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 3)
        self.horizontalLayout_4.setStretch(4, 1)
        self.horizontalLayout_4.setStretch(5, 3)
        self.horizontalLayout_4.setStretch(6, 1)
        self.horizontalLayout_4.setStretch(7, 3)
        self.horizontalLayout_4.setStretch(8, 1)
        self.horizontalLayout_4.setStretch(9, 3)
        self.tabWidget.addTab(self.tab_type, _fromUtf8(""))
        self.tab_search = QtGui.QWidget()
        self.tab_search.setObjectName(_fromUtf8("tab_search"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.tab_search)
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.radioButton_name = QtGui.QRadioButton(self.tab_search)
        self.radioButton_name.setObjectName(_fromUtf8("radioButton_name"))
        self.horizontalLayout_5.addWidget(self.radioButton_name)
        self.radioButton_author = QtGui.QRadioButton(self.tab_search)
        self.radioButton_author.setObjectName(_fromUtf8("radioButton_author"))
        self.horizontalLayout_5.addWidget(self.radioButton_author)
        self.radioButton_tags = QtGui.QRadioButton(self.tab_search)
        self.radioButton_tags.setObjectName(_fromUtf8("radioButton_tags"))
        self.horizontalLayout_5.addWidget(self.radioButton_tags)
        self.lineEdit_search = QtGui.QLineEdit(self.tab_search)
        self.lineEdit_search.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_search.setObjectName(_fromUtf8("lineEdit_search"))
        self.horizontalLayout_5.addWidget(self.lineEdit_search)
        self.tabWidget.addTab(self.tab_search, _fromUtf8(""))
        self.tab_cache = QtGui.QWidget()
        self.tab_cache.setObjectName(_fromUtf8("tab_cache"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_cache)
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_cache_status = QtGui.QLabel(self.tab_cache)
        self.label_cache_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cache_status.setObjectName(_fromUtf8("label_cache_status"))
        self.horizontalLayout_3.addWidget(self.label_cache_status)
        self.comboBox_cache_status = QtGui.QComboBox(self.tab_cache)
        self.comboBox_cache_status.setObjectName(_fromUtf8("comboBox_cache_status"))
        self.horizontalLayout_3.addWidget(self.comboBox_cache_status)
        self.label_cache_download = QtGui.QLabel(self.tab_cache)
        self.label_cache_download.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cache_download.setObjectName(_fromUtf8("label_cache_download"))
        self.horizontalLayout_3.addWidget(self.label_cache_download)
        self.comboBox_cache_download = QtGui.QComboBox(self.tab_cache)
        self.comboBox_cache_download.setObjectName(_fromUtf8("comboBox_cache_download"))
        self.horizontalLayout_3.addWidget(self.comboBox_cache_download)
        self.label_cache_msg = QtGui.QLabel(self.tab_cache)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_cache_msg.sizePolicy().hasHeightForWidth())
        self.label_cache_msg.setSizePolicy(sizePolicy)
        self.label_cache_msg.setText(_fromUtf8(""))
        self.label_cache_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cache_msg.setObjectName(_fromUtf8("label_cache_msg"))
        self.horizontalLayout_3.addWidget(self.label_cache_msg)
        self.pushButton_sync = QtGui.QPushButton(self.tab_cache)
        self.pushButton_sync.setObjectName(_fromUtf8("pushButton_sync"))
        self.horizontalLayout_3.addWidget(self.pushButton_sync)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(3, 3)
        self.horizontalLayout_3.setStretch(4, 9)
        self.horizontalLayout_3.setStretch(5, 1)
        self.tabWidget.addTab(self.tab_cache, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "免费小说书城 by Qin", None))
        self.groupBox_settings.setTitle(_translate("MainWindow", "设置", None))
        self.label_gender.setText(_translate("MainWindow", "性别", None))
        self.label_major.setText(_translate("MainWindow", "主类", None))
        self.label_minor.setText(_translate("MainWindow", "次类", None))
        self.label_status.setText(_translate("MainWindow", "状态", None))
        self.label_sort.setText(_translate("MainWindow", "排序", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_type), _translate("MainWindow", "分类", None))
        self.radioButton_name.setText(_translate("MainWindow", "书名", None))
        self.radioButton_author.setText(_translate("MainWindow", "作者", None))
        self.radioButton_tags.setText(_translate("MainWindow", "标签", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), _translate("MainWindow", "搜索", None))
        self.label_cache_status.setText(_translate("MainWindow", "状态", None))
        self.label_cache_download.setText(_translate("MainWindow", "下载", None))
        self.pushButton_sync.setText(_translate("MainWindow", "同步", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_cache), _translate("MainWindow", "缓存", None))
        self.groupBox_dump.setTitle(_translate("MainWindow", "转存", None))
        self.pushButton_before_page.setText(_translate("MainWindow", "<<", None))
        self.label_page_limit.setText(_translate("MainWindow", "/", None))
        self.pushButton_after_page.setText(_translate("MainWindow", ">>", None))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新", None))
        self.pushButton_remove.setText(_translate("MainWindow", "删除", None))
        self.pushButton_sources.setText(_translate("MainWindow", "书源", None))
        self.pushButton_start.setText(_translate("MainWindow", "开始", None))
        self.pushButton_stop.setText(_translate("MainWindow", "停止", None))

