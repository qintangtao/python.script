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
        MainWindow.resize(481, 575)
        MainWindow.setStyleSheet(_fromUtf8("QGroupBox{font-weight:bold;}"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(MainWindow)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_login = QtGui.QGroupBox(MainWindow)
        self.groupBox_login.setStyleSheet(_fromUtf8(""))
        self.groupBox_login.setObjectName(_fromUtf8("groupBox_login"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_login)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox_login)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_mobile = QtGui.QLineEdit(self.groupBox_login)
        self.lineEdit_mobile.setObjectName(_fromUtf8("lineEdit_mobile"))
        self.gridLayout.addWidget(self.lineEdit_mobile, 0, 1, 1, 2)
        self.label_4 = QtGui.QLabel(self.groupBox_login)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.lineEdit_smscode = QtGui.QLineEdit(self.groupBox_login)
        self.lineEdit_smscode.setObjectName(_fromUtf8("lineEdit_smscode"))
        self.gridLayout.addWidget(self.lineEdit_smscode, 1, 1, 1, 1)
        self.label_message = QtGui.QLabel(self.groupBox_login)
        self.label_message.setAlignment(QtCore.Qt.AlignCenter)
        self.label_message.setObjectName(_fromUtf8("label_message"))
        self.gridLayout.addWidget(self.label_message, 0, 3, 1, 3)
        self.pushButton_sendSmscode = QtGui.QPushButton(self.groupBox_login)
        self.pushButton_sendSmscode.setObjectName(_fromUtf8("pushButton_sendSmscode"))
        self.gridLayout.addWidget(self.pushButton_sendSmscode, 1, 2, 1, 1)
        self.pushButton_login = QtGui.QPushButton(self.groupBox_login)
        self.pushButton_login.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton_login.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_login.setObjectName(_fromUtf8("pushButton_login"))
        self.gridLayout.addWidget(self.pushButton_login, 1, 4, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_login)
        self.groupBox_settings = QtGui.QGroupBox(MainWindow)
        self.groupBox_settings.setObjectName(_fromUtf8("groupBox_settings"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_settings)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_6 = QtGui.QLabel(self.groupBox_settings)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_4.addWidget(self.label_6)
        self.lineEdit_path = QtGui.QLineEdit(self.groupBox_settings)
        self.lineEdit_path.setObjectName(_fromUtf8("lineEdit_path"))
        self.horizontalLayout_4.addWidget(self.lineEdit_path)
        self.pushButton_path = QtGui.QPushButton(self.groupBox_settings)
        self.pushButton_path.setObjectName(_fromUtf8("pushButton_path"))
        self.horizontalLayout_4.addWidget(self.pushButton_path)
        self.verticalLayout_3.addWidget(self.groupBox_settings)
        self.groupBox_cats = QtGui.QGroupBox(MainWindow)
        self.groupBox_cats.setObjectName(_fromUtf8("groupBox_cats"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_cats)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_gender = QtGui.QLabel(self.groupBox_cats)
        self.label_gender.setObjectName(_fromUtf8("label_gender"))
        self.horizontalLayout_2.addWidget(self.label_gender)
        self.comboBox_gender = QtGui.QComboBox(self.groupBox_cats)
        self.comboBox_gender.setObjectName(_fromUtf8("comboBox_gender"))
        self.horizontalLayout_2.addWidget(self.comboBox_gender)
        self.label = QtGui.QLabel(self.groupBox_cats)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox_major = QtGui.QComboBox(self.groupBox_cats)
        self.comboBox_major.setObjectName(_fromUtf8("comboBox_major"))
        self.horizontalLayout_2.addWidget(self.comboBox_major)
        self.label_2 = QtGui.QLabel(self.groupBox_cats)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_minor = QtGui.QComboBox(self.groupBox_cats)
        self.comboBox_minor.setObjectName(_fromUtf8("comboBox_minor"))
        self.horizontalLayout_2.addWidget(self.comboBox_minor)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 4)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 4)
        self.horizontalLayout_2.setStretch(4, 1)
        self.horizontalLayout_2.setStretch(5, 4)
        self.verticalLayout_3.addWidget(self.groupBox_cats)
        self.groupBox_type = QtGui.QGroupBox(MainWindow)
        self.groupBox_type.setObjectName(_fromUtf8("groupBox_type"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_type)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioButton_hot = QtGui.QRadioButton(self.groupBox_type)
        self.radioButton_hot.setObjectName(_fromUtf8("radioButton_hot"))
        self.horizontalLayout_3.addWidget(self.radioButton_hot)
        self.radioButton_new = QtGui.QRadioButton(self.groupBox_type)
        self.radioButton_new.setObjectName(_fromUtf8("radioButton_new"))
        self.horizontalLayout_3.addWidget(self.radioButton_new)
        self.radioButton_good = QtGui.QRadioButton(self.groupBox_type)
        self.radioButton_good.setObjectName(_fromUtf8("radioButton_good"))
        self.horizontalLayout_3.addWidget(self.radioButton_good)
        self.radioButton_done = QtGui.QRadioButton(self.groupBox_type)
        self.radioButton_done.setObjectName(_fromUtf8("radioButton_done"))
        self.horizontalLayout_3.addWidget(self.radioButton_done)
        self.radioButton_vip = QtGui.QRadioButton(self.groupBox_type)
        self.radioButton_vip.setObjectName(_fromUtf8("radioButton_vip"))
        self.horizontalLayout_3.addWidget(self.radioButton_vip)
        self.verticalLayout_3.addWidget(self.groupBox_type)
        self.groupBox_books = QtGui.QGroupBox(MainWindow)
        self.groupBox_books.setObjectName(_fromUtf8("groupBox_books"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_books)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_5 = QtGui.QLabel(self.groupBox_books)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEdit_start = QtGui.QLineEdit(self.groupBox_books)
        self.lineEdit_start.setObjectName(_fromUtf8("lineEdit_start"))
        self.horizontalLayout.addWidget(self.lineEdit_start)
        self.label_7 = QtGui.QLabel(self.groupBox_books)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout.addWidget(self.label_7)
        self.lineEdit_limit = QtGui.QLineEdit(self.groupBox_books)
        self.lineEdit_limit.setObjectName(_fromUtf8("lineEdit_limit"))
        self.horizontalLayout.addWidget(self.lineEdit_limit)
        self.checkBox_nextPage = QtGui.QCheckBox(self.groupBox_books)
        self.checkBox_nextPage.setObjectName(_fromUtf8("checkBox_nextPage"))
        self.horizontalLayout.addWidget(self.checkBox_nextPage)
        self.pushButton_refresh = QtGui.QPushButton(self.groupBox_books)
        self.pushButton_refresh.setObjectName(_fromUtf8("pushButton_refresh"))
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.listWidget_books = QtGui.QListWidget(self.groupBox_books)
        self.listWidget_books.setEnabled(True)
        self.listWidget_books.setObjectName(_fromUtf8("listWidget_books"))
        self.horizontalLayout_6.addWidget(self.listWidget_books)
        self.listWidget_dump = QtGui.QListWidget(self.groupBox_books)
        self.listWidget_dump.setObjectName(_fromUtf8("listWidget_dump"))
        self.horizontalLayout_6.addWidget(self.listWidget_dump)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.groupBox_books)
        self.groupBox_dump = QtGui.QGroupBox(MainWindow)
        self.groupBox_dump.setObjectName(_fromUtf8("groupBox_dump"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_dump)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_title_author = QtGui.QLabel(self.groupBox_dump)
        self.label_title_author.setText(_fromUtf8(""))
        self.label_title_author.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_title_author.setObjectName(_fromUtf8("label_title_author"))
        self.horizontalLayout_5.addWidget(self.label_title_author)
        self.checkBox_auto = QtGui.QCheckBox(self.groupBox_dump)
        self.checkBox_auto.setObjectName(_fromUtf8("checkBox_auto"))
        self.horizontalLayout_5.addWidget(self.checkBox_auto)
        self.checkBox_log = QtGui.QCheckBox(self.groupBox_dump)
        self.checkBox_log.setObjectName(_fromUtf8("checkBox_log"))
        self.horizontalLayout_5.addWidget(self.checkBox_log)
        self.pushButton_start = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_start.setObjectName(_fromUtf8("pushButton_start"))
        self.horizontalLayout_5.addWidget(self.pushButton_start)
        self.pushButton_stop = QtGui.QPushButton(self.groupBox_dump)
        self.pushButton_stop.setObjectName(_fromUtf8("pushButton_stop"))
        self.horizontalLayout_5.addWidget(self.pushButton_stop)
        self.horizontalLayout_5.setStretch(0, 4)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(3, 1)
        self.horizontalLayout_5.setStretch(4, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.textEdit_log = QtGui.QTextEdit(self.groupBox_dump)
        self.textEdit_log.setObjectName(_fromUtf8("textEdit_log"))
        self.verticalLayout_2.addWidget(self.textEdit_log)
        self.verticalLayout_3.addWidget(self.groupBox_dump)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "追书神器", None))
        self.groupBox_login.setTitle(_translate("MainWindow", "登录", None))
        self.label_3.setText(_translate("MainWindow", "手机号", None))
        self.label_4.setText(_translate("MainWindow", "验证码", None))
        self.label_message.setText(_translate("MainWindow", "请登录...", None))
        self.pushButton_sendSmscode.setText(_translate("MainWindow", "发送", None))
        self.pushButton_login.setText(_translate("MainWindow", "登录", None))
        self.groupBox_settings.setTitle(_translate("MainWindow", "设置", None))
        self.label_6.setText(_translate("MainWindow", "路径", None))
        self.pushButton_path.setText(_translate("MainWindow", "...", None))
        self.groupBox_cats.setTitle(_translate("MainWindow", "分类", None))
        self.label_gender.setText(_translate("MainWindow", "性别", None))
        self.label.setText(_translate("MainWindow", "主类", None))
        self.label_2.setText(_translate("MainWindow", "次类", None))
        self.groupBox_type.setTitle(_translate("MainWindow", "类型", None))
        self.radioButton_hot.setText(_translate("MainWindow", "热门", None))
        self.radioButton_new.setText(_translate("MainWindow", "新书", None))
        self.radioButton_good.setText(_translate("MainWindow", "好评", None))
        self.radioButton_done.setText(_translate("MainWindow", "完结", None))
        self.radioButton_vip.setText(_translate("MainWindow", "VIP", None))
        self.groupBox_books.setTitle(_translate("MainWindow", "列表", None))
        self.label_5.setText(_translate("MainWindow", "起始页", None))
        self.label_7.setText(_translate("MainWindow", "页大小", None))
        self.checkBox_nextPage.setText(_translate("MainWindow", "下一页", None))
        self.pushButton_refresh.setText(_translate("MainWindow", "刷新", None))
        self.groupBox_dump.setTitle(_translate("MainWindow", "转存", None))
        self.checkBox_auto.setText(_translate("MainWindow", "自动", None))
        self.checkBox_log.setText(_translate("MainWindow", "日志", None))
        self.pushButton_start.setText(_translate("MainWindow", "开始", None))
        self.pushButton_stop.setText(_translate("MainWindow", "停止", None))

