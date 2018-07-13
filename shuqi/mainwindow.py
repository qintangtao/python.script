#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import res
import scapi
import data
import utils
from PyQt4 import QtGui, QtCore
from ui_mainwindow import Ui_MainWindow
from threads import SearchThread, SourcesThread, DumpThread
from model import BookState, BookTableModel
from delegate import BookItemDelegate


def gbk2utf8(txt):
    return unicode(txt, 'gbk').encode('utf-8')


def utf82gbk(txt):
    return unicode(txt, 'utf-8').encode('gbk')


def qstr2str(txt):
    return unicode(txt.toUtf8(), 'utf8', 'ignore')


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.max_dump_count = 3
        self.page_index = 0
        self.page_total = 0
        self.page_limit = 10
        self.uid = utils.generate_uid()
        self.path = os.path.join(os.getcwd(), 'dump')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.__init_ui()

    def __init_ui(self):
        self.setWindowIcon(QtGui.QIcon(':/bug.ico'))
        # self.connect(self.ui.tableView, QtCore.SIGNAL(
        #    'doubleClicked(QModelIndex)'), self.onDoubleClicked)
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
        self.ui.pushButton_remove.clicked.connect(self.onRemoveClicked)
        self.ui.pushButton_sources.clicked.connect(self.onSourcesClicked)
        self.ui.pushButton_start.clicked.connect(self.onStartClicked)
        self.ui.pushButton_stop.clicked.connect(self.onStopClicked)
        self.ui.lineEdit_page_index.setText(str(self.page_index))
        self.ui.lineEdit_page_total.setText(str(self.page_total))
        self.ui.lineEdit_page_index.setEnabled(False)
        self.ui.lineEdit_page_total.setEnabled(False)
        self.ui.pushButton_before_page.setEnabled(False)
        self.ui.pushButton_after_page.setEnabled(False)
        self.ui.pushButton_remove.setEnabled(False)
        self.ui.pushButton_sources.setEnabled(False)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)
        self.model = BookTableModel(self)
        self.ui.tableView.setModel(self.model)
        self.delegate = BookItemDelegate(self)
        self.ui.tableView.setItemDelegate(self.delegate)
        self.ui.tableView.setEditTriggers(
            QtGui.QAbstractItemView.DoubleClicked)
        # self.ui.tableView.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.ui.tableView.setSelectionBehavior(
            QtGui.QAbstractItemView.SelectRows)
        self.ui.tableView.horizontalHeader().setClickable(False)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)
        self.ui.tableView.horizontalHeader().setMovable(False)
        self.ui.tableView.horizontalHeader().setSelectionMode(
            QtGui.QAbstractItemView.NoSelection)
        self.__init_gender()
        self.__init_status_sort()
        self.__init_dump()

    def __init_dump(self):
        self.listdump = []
        for i in xrange(0, self.max_dump_count):
            dump = DumpThread()
            dump.signal_log.connect(self.onSignalLog)
            dump.signal_progress.connect(self.onSignalProgress)
            dump.signal_finished.connect(self.onSignalFinished)
            self.listdump.append(dump)

    def __init_status_sort(self):
        status_list = scapi.get_status_list()
        for item in status_list:
            self.ui.comboBox_status.addItem(item['name'])

        sort_list = scapi.get_sort_list()
        for item in sort_list:
            self.ui.comboBox_sort.addItem(item['name'])

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
            0, self.ui.tableView.width() * 20 / 100)
        self.ui.tableView.setColumnWidth(
            1, self.ui.tableView.width() * 14 / 100)
        self.ui.tableView.setColumnWidth(
            2, self.ui.tableView.width() * 10 / 100)
        self.ui.tableView.setColumnWidth(
            3, self.ui.tableView.width() * 15 / 100)
        self.ui.tableView.setColumnWidth(
            4, self.ui.tableView.width() * 13 / 100)

    def __request_books(self):
        major = qstr2str(self.ui.comboBox_major.currentText())
        minor = qstr2str(self.ui.comboBox_minor.currentText())
        if minor == u'全部':
            minor = ''

        status = ''
        status_name = qstr2str(self.ui.comboBox_status.currentText())
        status_list = scapi.get_status_list()
        for item in status_list:
            if item['name'] == status_name:
                status = item['flag']
                break

        sort = ''
        sort_name = qstr2str(self.ui.comboBox_sort.currentText())
        sort_list = scapi.get_sort_list()
        for item in sort_list:
            if item['name'] == sort_name:
                sort = item['flag']
                break

        self.search = SearchThread(self)
        self.search.signal_search.connect(self.onSignalSearch)
        self.search.signal_finished.connect(self.onSignalSearchFinished)
        self.search.start(self.uid, major, minor, status,
                          sort, self.page_index * self.page_limit, self.page_limit)

        self.model.updateData([])
        self.__enabledComboBox(False)
        self.__enabledPageButton(False)
        self.ui.pushButton_refresh.setEnabled(False)
        self.ui.pushButton_remove.setEnabled(False)
        self.ui.pushButton_sources.setEnabled(False)
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)

    def __enabledComboBox(self, enabled):
        self.ui.comboBox_gender.setEnabled(enabled)
        self.ui.comboBox_major.setEnabled(enabled)
        self.ui.comboBox_minor.setEnabled(enabled)
        self.ui.comboBox_status.setEnabled(enabled)
        self.ui.comboBox_sort.setEnabled(enabled)

    def __enabledPageButton(self, enabled=True):
        if enabled:
            self.ui.pushButton_before_page.setEnabled(
                True if self.page_index > 0 else False)
            self.ui.lineEdit_page_index.setEnabled(enabled)
            self.ui.pushButton_before_page.setEnabled(
                True if self.page_index + 1 < self.page_total else False)
        else:
            self.ui.pushButton_before_page.setEnabled(enabled)
            self.ui.lineEdit_page_index.setEnabled(enabled)
            self.ui.pushButton_after_page.setEnabled(enabled)

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
        for dump in self.listdump:
            if dump.isRunning():
                return
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

    def onSignalSearch(self, total, listdata):
        self.page_total = total / \
            self.page_limit if total % self.page_limit == 0 else total / self.page_limit + 1
        for item in listdata:
            item['site'] = ''
            item['sources'] = []
            item['progress'] = ''
            item['log'] = ''
            item['state'] = BookState.Free
        self.model.updateData(listdata)

    def onSignalSearchFinished(self, code):
        if code == 0:
            self.ui.lineEdit_page_index.setText(str(self.page_index+1))
            self.ui.lineEdit_page_total.setText(str(self.page_total))
            self.ui.pushButton_remove.setEnabled(True)
            self.ui.pushButton_sources.setEnabled(True)
            self.ui.pushButton_start.setEnabled(False)
            self.__enabledPageButton()
        self.__enabledComboBox(True)
        self.ui.pushButton_refresh.setEnabled(True)

    def onRemoveClicked(self):
        bids = []
        selectedIndexes = self.ui.tableView.selectionModel().selectedIndexes()
        for index in selectedIndexes:
            bids.append(self.model.getId(index.row()))
        for bid in bids:
            row = self.model.getRowById(bid)
            self.model.removeRow(row)

        if self.model.rowCount() == 0:
            self.ui.pushButton_remove.setEnabled(False)
            self.ui.pushButton_sources.setEnabled(False)

    def onSourcesClicked(self):
        self.rowSources = 0
        if self.model.rowCount() > self.rowSources:
            self.model.setLog(self.rowSources, u'请求书源...')
            self.sources = SourcesThread(self)
            self.sources.signal_sources.connect(self.onSignalSources)
            self.sources.signal_finished.connect(self.onSignalSourcesFinished)
            self.model.setState(self.rowSources, BookState.Dumping)
            self.sources.start(self.rowSources, self.model.getId(
                self.rowSources), self.uid)
            self.__enabledComboBox(False)
            self.__enabledPageButton(False)
            self.ui.pushButton_refresh.setEnabled(False)
            self.ui.pushButton_remove.setEnabled(False)
            self.ui.pushButton_sources.setEnabled(False)

    def onSignalSources(self, index, sources):
        self.model.setSources(index, sources)

    def onSignalSourcesFinished(self, index, code):
        if code == 0:
            self.model.setLog(index, '')
            self.model.setState(index, BookState.Free)
        elif code == 1:
            self.model.setLog(index, 'Failure')
            self.model.setState(index, BookState.Failure)
        else:
            self.model.setLog(index, 'Stop')
            self.model.setState(index, BookState.Free)

        if code != 2:
            self.rowSources = self.rowSources + 1
            if self.model.rowCount() > self.rowSources:
                self.model.setLog(self.rowSources, u'请求书源...')
                self.model.setState(self.rowSources, BookState.Dumping)
                self.sources.start(self.rowSources, self.model.getId(
                    self.rowSources), self.uid)
            else:
                self.__enabledComboBox(True)
                self.__enabledPageButton()
                self.ui.pushButton_refresh.setEnabled(True)
                self.ui.pushButton_remove.setEnabled(True)
                self.ui.pushButton_sources.setEnabled(True)
                self.ui.pushButton_start.setEnabled(True)
                self.ui.pushButton_stop.setEnabled(False)

    def onStartClicked(self):
        if self.model.rowCount() > 0:
            self.model.setAllState(BookState.Failure, BookState.Free)
            for dump in self.listdump:
                row = self.model.getFreeRow()
                if row == -1:
                    break
                bid = self.model.getId(row)
                source = self.model.getSources(row)
                self.model.setState(row, BookState.Dumping)
                dump.start(row, self.path, bid, self.uid,
                           source['site'], source['site_name'])

            self.__enabledComboBox(False)
            self.__enabledPageButton(False)
            self.ui.pushButton_refresh.setEnabled(False)
            self.ui.pushButton_remove.setEnabled(False)
            self.ui.pushButton_sources.setEnabled(False)
            self.ui.pushButton_start.setEnabled(False)
            self.ui.pushButton_stop.setEnabled(True)

    def onStopClicked(self):
        for dump in self.listdump:
            dump.stop()
        self.ui.pushButton_stop.setEnabled(False)

        for dump in self.listdump:
            if dump.isRunning():
                return

        self.__enabledComboBox(True)
        self.__enabledPageButton()
        self.ui.pushButton_refresh.setEnabled(True)
        self.ui.pushButton_remove.setEnabled(True)
        self.ui.pushButton_sources.setEnabled(True)
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)

    def onSignalLog(self, index, log):
        self.model.setLog(index, log)

    def onSignalProgress(self, index, total, current):
        self.model.setProgress(index, "%d/%d" % (current+1, total))

    def onSignalFinished(self, index, code):
        if code == 0:
            self.model.setLog(index, 'Success')
            self.model.setState(index, BookState.Success)
        elif code == 1:
            self.model.setLog(index, 'Failure')
            self.model.setState(index, BookState.Failure)
        else:
            self.model.setLog(index, 'Stop')
            self.model.setState(index, BookState.Free)

        if code != 2:
            row = self.model.getFreeRow()
            if row > -1:
                bid = self.model.getId(row)
                self.model.setState(row, BookState.Dumping)
                source = self.model.getSources(row)
                self.sender().start(row, self.path, bid, self.uid,
                                    source['site'], source['site_name'])

        else:
            for dump in self.listdump:
                if dump.isRunning():
                    return

            self.__enabledComboBox(True)
            self.__enabledPageButton()
            self.ui.pushButton_refresh.setEnabled(True)
            self.ui.pushButton_remove.setEnabled(True)
            self.ui.pushButton_sources.setEnabled(True)
            self.ui.pushButton_start.setEnabled(True)
            self.ui.pushButton_stop.setEnabled(False)
