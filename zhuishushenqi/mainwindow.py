#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import zsapi
import res
from PyQt4 import QtGui, QtCore
from ui_mainwindow import Ui_MainWindow
from config import ConfigFile
from dump import DumpThread


def gbk2utf8(txt):
    return unicode(txt, 'gbk').encode('utf-8')


def utf82gbk(txt):
    return unicode(txt, 'utf-8').encode('gbk')


def qstr2str(txt):
    return unicode(txt.toUtf8(), 'utf8', 'ignore')


def logging_config(path, level):
    t = time.localtime(time.time())
    path = os.path.join(path, 'log')
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, 'dump_%d%02d%02d.log' %
                            (t.tm_year, t.tm_mon, t.tm_mday))
    logging.basicConfig(level=level,
                        format='{%(funcName)s:%(lineno)d} <%(levelname)s> %(message)s',
                        filename=filename,
                        filemode='a')


def logging_level(level):
    if level is not None:
        level = level.upper()
    if level == 'CRITICAL':
        return logging.CRITICAL
    if level == 'FATAL':
        return logging.FATAL
    if level == 'ERROR':
        return logging.ERROR
    if level == 'WARNING':
        return logging.WARNING
    if level == 'WARN':
        return logging.WARN
    if level == 'INFO':
        return logging.INFO
    if level == 'DEBUG':
        return logging.DEBUG
    return logging.NOTSET


def logging_set_level(level):
    root = logging.getLogger()
    root.setLevel(level)


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.path = os.getcwd()
        logging_config(self.path, logging_level('info'))
        self.conf = ConfigFile(os.path.join(self.path, 'config.ini'))
        self.dict_gender = {'male': u"男生", 'female': u"女生",
                            'picture': u"漫画", 'press': u"出版"}
        self.__init_ui()

    def __init_ui(self):
        self.setWindowIcon(QtGui.QIcon(':/bug.ico'))
        self.connect(self.ui.comboBox_gender, QtCore.SIGNAL(
            'activated(QString)'), self.onComboBoxGenderActivated)
        self.connect(self.ui.comboBox_major, QtCore.SIGNAL(
            'activated(QString)'), self.onComboBoxMajorActivated)
        self.connect(self.ui.listWidget_books, QtCore.SIGNAL(
            'itemDoubleClicked(QListWidgetItem*)'), self.onListBooksItemDoubleClicked)
        self.connect(self.ui.listWidget_dump, QtCore.SIGNAL(
            'itemDoubleClicked(QListWidgetItem*)'), self.onListDumpItemDoubleClicked)
        self.ui.pushButton_refresh.clicked.connect(self.onRefreshClicked)
        self.ui.pushButton_start.clicked.connect(self.onStartClicked)
        self.ui.pushButton_stop.clicked.connect(self.onStopClicked)
        self.ui.checkBox_auto.stateChanged.connect(self.onAutoStateChanged)
        self.ui.checkBox_log.stateChanged.connect(self.onLogStateChanged)
        self.ui.groupBox_books.setVisible(False)
        self.ui.checkBox_auto.setChecked(True)
        self.ui.radioButton_vip.setChecked(True)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        path = self.get_path()
        if not os.path.exists(path):
            path = self.path
        self.ui.lineEdit_path.setText(path)
        self.ui.lineEdit_start.setText(str(self.get_start()))
        self.ui.lineEdit_limit.setText(str(self.get_limit()))
        self.set_selected_type(self.get_type())
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.onTimer)
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    def __init_login(self):
        token = self.conf.user_token
        if token is not None and token.strip != '':
            if zsapi.request_account(token):
                self.token = token
                return True

        token = zsapi.request_login(
            self.conf.login_platform_uid,
            self.conf.login_channelName,
            self.conf.login_packageName,
            self.conf.login_promoterId,
            self.conf.login_platform_token,
            self.conf.login_platform_code,
            self.conf.login_version)
        if token is not None and token.strip != '':
            self.conf.user_token = token
            self.token = token
            return True

        return False

    def __init_cats(self):
        self.json_cats = zsapi.request_cats_lv2()
        if self.json_cats is not None and self.json_cats['ok'] is True:
            self.__init_cats_gender()
        else:
            logging.error('request_cats_lv2 error')

    def __init_cats_gender(self):
        if self.json_cats is not None:
            gender = self.get_gender()
            i = 0
            currentIndex = 0
            for key in self.dict_gender:
                if self.json_cats[key] is not None:
                    self.ui.comboBox_gender.addItem(self.dict_gender[key])
                    if gender == '':
                        gender = key
                    elif gender == key:
                        currentIndex = i
                i += 1
            self.ui.comboBox_gender.setCurrentIndex(currentIndex)
            self.__init_cats_major(gender)

    def __init_cats_major(self, gender):
        self.ui.comboBox_major.clear()
        major = ''
        if gender == self.get_gender():
            major = self.get_major()
        i = 0
        currentIndex = 0
        for item in self.json_cats[gender]:
            self.ui.comboBox_major.addItem(item['major'])
            if major == '':
                major = item['major']
            elif major == item['major']:
                currentIndex = i
            i += 1
        self.ui.comboBox_major.setCurrentIndex(currentIndex)
        self.__init_cats_minor(gender, major)

    def __init_cats_minor(self, gender, major):
        self.ui.comboBox_minor.clear()
        for item in self.json_cats[gender]:
            if item['major'] == major:
                minor = ''
                if gender == self.get_gender() and major == self.get_major():
                    minor = self.get_minor()
                i = 0
                currentIndex = 0
                self.ui.comboBox_minor.addItem(u"全部")
                i += 1
                for item2 in item['mins']:
                    self.ui.comboBox_minor.addItem(item2)
                    if minor == '':
                        minor = item2
                    elif minor == item2:
                        currentIndex = i
                    i += 1
                self.ui.comboBox_minor.setCurrentIndex(currentIndex)

    def str2gender(self, _str):
        for key in self.dict_gender:
            if self.dict_gender[key] == _str:
                return key
        return None

    def set_logging(self, enabled):
        logging_set_level(logging_level('debug' if enabled else 'info'))

    def get_gender(self):
        gender = self.conf.dump_gender
        if gender is None or gender.strip() == '':
            gender = ''
            self.conf.dump_gender = gender
        return gender

    def get_type(self):
        _type = self.conf.dump_type
        if _type is None or _type.strip() == '':
            _type = ''
            self.conf.dump__type = _type
        return _type

    def get_start(self):
        start = self.conf.dump_start
        if start is None or start.strip() == '':
            start = 0
            self.conf.dump_start = start
        return int(start)

    def get_limit(self):
        limit = self.conf.dump_limit
        if limit is None or limit.strip() == '':
            limit = 5
            self.conf.dump_limit = limit
        return int(limit)

    def get_major(self):
        major = self.conf.dump_major
        if major is None or major.strip() == '':
            major = ''
            self.conf.dump_major = major
        return major

    def get_minor(self):
        minor = self.conf.dump_minor
        if minor is None:
            minor = ''
            self.conf.dump_minor = minor
        return minor

    def get_path(self):
        path = self.conf.dump_path
        if path is None:
            path = os.getcwd()
            self.conf.dump_path = path
        return path

    def get_selected_type(self):
        return 'monthly'
        if self.ui.radioButton_hot.isChecked():
            return 'hot'
        if self.ui.radioButton_new.isChecked():
            return 'new'
        if self.ui.radioButton_good.isChecked():
            return 'reputation'
        if self.ui.radioButton_done.isChecked():
            return 'over'
        if self.ui.radioButton_vip.isChecked():
            return 'monthly'
        return 'hot'

    def set_selected_type(self, _type):
        if _type == 'hot':
            self.ui.radioButton_hot.setChecked(True)
        elif _type == 'new':
            self.ui.radioButton_new.setChecked(True)
        elif _type == 'reputation':
            self.ui.radioButton_good.setChecked(True)
        elif _type == 'over':
            self.ui.radioButton_done.setChecked(True)
        elif _type == 'monthly':
            self.ui.radioButton_vip.setChecked(True)
        else:
            self.ui.radioButton_vip.setChecked(True)

    def onComboBoxGenderActivated(self, text):
        gender = self.str2gender(qstr2str(text))
        if gender is not None:
            self.__init_cats_major(gender)

    def onComboBoxMajorActivated(self, text):
        gender = self.str2gender(
            qstr2str(self.ui.comboBox_gender.currentText()))
        if gender is not None:
            self.__init_cats_minor(gender, text)

    def onLogin(self, ok):
        if ok:
            self.ui.label_message.setText(u"登陆成功")
            self.__init_cats()
        else:
            self.ui.label_message.setText(u"登陆失败")

    def onTimer(self):
        self.ui.label_message.setText(u"登陆中...")
        if self.__init_login():
            self.ui.label_message.setText(u"登陆成功")
            self.__init_cats()
        else:
            self.ui.label_message.setText(u"登陆失败")

    def onRefreshClicked(self):
        path = str(self.ui.lineEdit_path.text())
        gender = self.str2gender(
            qstr2str(self.ui.comboBox_gender.currentText()))
        major = qstr2str(self.ui.comboBox_major.currentText())
        minor = '' if self.ui.comboBox_minor.currentIndex(
        ) == 0 else qstr2str(self.ui.comboBox_minor.currentText())
        __type = self.get_selected_type()
        start = int(self.ui.lineEdit_start.text())
        limit = int(self.ui.lineEdit_limit.text())

        if self.ui.checkBox_nextPage.isChecked():
            start += 1
            self.ui.lineEdit_start.setText(str(start))

        self.conf.dump_path = path
        self.conf.dump_gender = gender
        self.conf.dump_type = __type
        self.conf.dump_major = major
        self.conf.dump_minor = minor
        self.conf.dump_start = start
        self.conf.dump_limit = limit
        self.conf.sync()

        self.dumpThread = DumpThread(
            self.token, path, gender, __type, major, minor, start, limit)
        self.dumpThread.signal_list.connect(self.onSignalList)
        self.dumpThread.signal_log.connect(self.onSignalLog)
        self.dumpThread.dump = False
        self.dumpThread.start()
        self.ui.listWidget_books.clear()
        self.ui.textEdit_log.clear()

    def onStartClicked(self):
        path = str(self.ui.lineEdit_path.text())
        gender = self.str2gender(
            qstr2str(self.ui.comboBox_gender.currentText()))
        major = qstr2str(self.ui.comboBox_major.currentText())
        minor = '' if self.ui.comboBox_minor.currentIndex(
        ) == 0 else qstr2str(self.ui.comboBox_minor.currentText())
        __type = self.get_selected_type()
        start = int(self.ui.lineEdit_start.text())
        limit = int(self.ui.lineEdit_limit.text())

        self.conf.dump_path = path
        self.conf.dump_gender = gender
        self.conf.dump_type = __type
        self.conf.dump_major = major
        self.conf.dump_minor = minor
        self.conf.dump_start = start
        self.conf.dump_limit = limit
        self.conf.sync()

        self.dumpThread = DumpThread(
            self.token, path, gender, __type, major, minor, start, limit)
        self.dumpThread.signal_start.connect(self.onSignalStart)
        self.dumpThread.signal_title.connect(self.onSignalTitle)
        self.dumpThread.signal_log.connect(self.onSignalLog)
        self.dumpThread.dump = True
        self.dumpThread.json = None
        self.dumpThread.start()
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)

    def onStopClicked(self):
        self.dumpThread.stop()
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def onSignalList(self, json):
        self.ui.listWidget_books.clear()
        for item in json:
            self.ui.listWidget_books.addItem(
                "%s-%s" % (item['title'], item['author']))

    def onSignalStart(self, start):
        self.conf.dump_start = start

    def onSignalTitle(self, txt):
        self.ui.label_title_author.setText(txt)
        self.ui.textEdit_log.clear()

    def onSignalLog(self, txt):
        self.ui.textEdit_log.append(txt)

    def onAutoStateChanged(self, state):
        # self.ui.groupBox_books.setVisible(
        #    False if state == QtCore.Qt.Checked else True)
        pass

    def onLogStateChanged(self, state):
        self.set_logging(True if state == QtCore.Qt.Checked else False)

    def onListBooksItemDoubleClicked(self, item):
        self.ui.listWidget_dump.addItem(item.text())

    def onListDumpItemDoubleClicked(self, item):
        self.ui.listWidget_dump.takeItem(self.ui.listWidget_dump.currentRow())
