#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
import logging
import res
import scapi
import data
from PyQt4 import QtGui, QtCore
from ui_mainwindow import Ui_MainWindow
from dump import DumpThread
from model import BookState, BookTableModel


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
        self.max_dump_count = 3
        self.page_index = 0
        self.page_total = 0
        self.page_limit = 10
        self.uid = scapi.generate_uid()
        self.__init_ui()

    def __init_ui(self):
        logging_config(os.getcwd(), logging_level('info'))
        self.setWindowIcon(QtGui.QIcon(':/bug.ico'))
        self.connect(self.ui.tableView, QtCore.SIGNAL(
            'doubleClicked(QModelIndex)'), self.onDoubleClicked)
        self.connect(self.ui.comboBox_gender, QtCore.SIGNAL(
            'activated(QString)'), self.onComboBoxGenderActivated)
        self.connect(self.ui.comboBox_major, QtCore.SIGNAL(
            'activated(QString)'), self.onComboBoxMajorActivated)
        self.ui.lineEdit_page_index.returnPressed.connect(
            self.onPageIndexReturnPressed)
        self.ui.pushButton_before_page.clicked.connect(
            self.onBeforePageClicked)
        self.ui.pushButton_after_page.clicked.connect(self.onAfterPageClicked)
        self.ui.pushButton_refresh.clicked.connect(self.onRefreshClicked)
        self.ui.pushButton_start.clicked.connect(self.onStartClicked)
        self.ui.pushButton_stop.clicked.connect(self.onStopClicked)
        self.ui.lineEdit_page_index.setText(str(self.page_index))
        self.ui.lineEdit_page_total.setText(str(self.page_total))
        self.ui.lineEdit_page_total.setEnabled(False)
        self.ui.pushButton_before_page.setEnabled(False)
        self.ui.pushButton_after_page.setEnabled(False)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        self.model = BookTableModel(self)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers)
        self.ui.tableView.setSelectionMode(
            QtGui.QAbstractItemView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.ui.tableView.horizontalHeader().setClickable(False)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.horizontalHeader().setMovable(False)
        self.ui.tableView.horizontalHeader().setSelectionMode(
            QtGui.QAbstractItemView.NoSelection)
        self.__init_gender()
        self.__init_dump()

    def __init_dump(self):
        self.listdump = []
        for i in xrange(0, self.max_dump_count):
            dump = DumpThread()
            dump.signal_log.connect(self.onSignalLog)
            dump.signal_progress.connect(self.onSignalProgress)
            dump.signal_finished.connect(self.onSignalFinished)
            self.listdump.append(dump)

    def __init_gender(self):
        self.ui.comboBox_gender.clear()
        for gender_item in data.book:
            self.ui.comboBox_gender.addItem(gender_item['name'])
        self.__init_major(self.ui.comboBox_gender.currentText())

    def __init_major(self, gender):
        self.ui.comboBox_major.clear()
        for gender_item in data.book:
            if gender_item['name'] == gender:
                for major_item in gender_item['major']:
                    self.ui.comboBox_major.addItem(major_item['name'])
                break
        self.__init_minor(gender, self.ui.comboBox_major.currentText())

    def __init_minor(self, gender, major):
        self.ui.comboBox_minor.clear()
        for gender_item in data.book:
            if gender_item['name'] == gender:
                for major_item in gender_item['major']:
                    if major_item['name'] == major:
                        self.ui.comboBox_minor.addItem(u'全部')
                        for minor in major_item['minor']:
                            self.ui.comboBox_minor.addItem(minor)
                        break
                break

    def __set_table_column_width(self):
        self.ui.tableView.setColumnWidth(
            0, self.ui.tableView.width() * 25 / 100)
        self.ui.tableView.setColumnWidth(
            1, self.ui.tableView.width() * 20 / 100)
        self.ui.tableView.setColumnWidth(
            2, self.ui.tableView.width() * 20 / 100)

    def __request_books(self):
        major = qstr2str(self.ui.comboBox_major.currentText())
        minor = qstr2str(self.ui.comboBox_minor.currentText())
        if minor == u'全部':
            minor = ''
        listdata = []
        json = scapi.request_Search(
            self.uid, major, minor, self.page_index * self.page_limit, self.page_limit)
        if json is not None and json['errno'] == 0:
            total = json['total']
            self.page_total = total / \
                self.page_limit if total % self.page_limit == 0 else total / self.page_limit + 1
            for item in json['data']:
                listdata.append({'id': item['id'], 'title': item['name'], 'author': item[
                                'author'], 'progress': '', 'log': u'双击删除此行', 'state': BookState.Free})
        self.model.updateData(listdata)

        self.ui.lineEdit_page_index.setText(str(self.page_index+1))
        self.ui.lineEdit_page_total.setText(str(self.page_total))

        if self.page_index > 0:
            self.ui.pushButton_before_page.setEnabled(True)
        else:
            self.ui.pushButton_before_page.setEnabled(False)

        if self.page_index + 1 < self.page_total:
            self.ui.pushButton_after_page.setEnabled(True)
        else:
            self.ui.pushButton_after_page.setEnabled(False)

    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        self.__set_table_column_width()

    def resizeEvent(self, event):
        super(MainWindow, self).resizeEvent(event)
        self.__set_table_column_width()

    def onComboBoxGenderActivated(self, text):
        self.__init_major(qstr2str(text))

    def onComboBoxMajorActivated(self, text):
        self.__init_minor(
            qstr2str(self.ui.comboBox_gender.currentText()), qstr2str(text))

    def onDoubleClicked(self, index):
        self.model.removeRow(index.row())

    def onPageIndexReturnPressed(self):
        if self.page_total > 0:
            try:
                page_index = int(self.ui.lineEdit_page_index.text())
                if page_index < 1 or page_index > self.page_total:
                    self.ui.lineEdit_page_index.setText(str(self.page_index+1))
                else:
                    self.page_index = page_index - 1
                    self.__request_books()
            except Exception:
                self.ui.lineEdit_page_index.setText(str(self.page_index+1))
        else:
            self.ui.lineEdit_page_index.setText(str(self.page_index))

    def onBeforePageClicked(self):
        self.page_index -= 1
        self.__request_books()

    def onAfterPageClicked(self):
        self.page_index += 1
        self.__request_books()

    def onRefreshClicked(self):
        self.__set_table_column_width()
        self.__request_books()

    def onStartClicked(self):
        if self.model.rowCount() > 0:
            path = os.path.join(os.getcwd(), 'dump')
            if not os.path.exists(path):
                os.makedirs(path)

            for dump in self.listdump:
                row = self.model.getFreeRow()
                if row == -1:
                    break
                bid = self.model.getId(row)
                self.model.setState(row, BookState.Dumping)
                dump.start(row, path, bid, self.uid)

            self.ui.comboBox_gender.setEnabled(False)
            self.ui.comboBox_major.setEnabled(False)
            self.ui.comboBox_minor.setEnabled(False)
            self.ui.lineEdit_page_index.setEnabled(False)
            self.ui.pushButton_before_page.setEnabled(False)
            self.ui.pushButton_after_page.setEnabled(False)
            self.ui.pushButton_refresh.setEnabled(False)
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(True)

    def onStopClicked(self):
        for dump in self.listdump:
            dump.stop()
        self.ui.comboBox_gender.setEnabled(True)
        self.ui.comboBox_major.setEnabled(True)
        self.ui.comboBox_minor.setEnabled(True)
        self.ui.lineEdit_page_index.setEnabled(True)
        self.ui.pushButton_refresh.setEnabled(True)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

        if self.page_index > 0:
            self.ui.pushButton_before_page.setEnabled(True)
        else:
            self.ui.pushButton_before_page.setEnabled(False)

        if self.page_index + 1 < self.page_total:
            self.ui.pushButton_after_page.setEnabled(True)
        else:
            self.ui.pushButton_after_page.setEnabled(False)

    def onSignalLog(self, index, log):
        self.model.setLog(index, log)

    def onSignalProgress(self, index, total, current):
        self.model.setProgress(index, "%d/%d" % (current+1, total))

    def onSignalFinished(self, index, code):
        if code == 0:
            self.model.setLog(index, 'Success')
            self.model.setState(index, BookState.Success)
            row = self.model.getFreeRow()
            if row > -1:
                bid = self.model.getId(row)
                self.model.setState(row, BookState.Dumping)
                self.sender().start(row, os.getcwd(), bid, self.uid)
        elif code == 1:
            self.model.setLog(index, 'Failure')
            self.model.setState(index, BookState.Failure)
        else:
            self.model.setLog(index, 'Stop')
            self.model.setState(index, BookState.Free)