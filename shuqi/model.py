#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PyQt4 import QtGui, QtCore
from enum import Enum, IntEnum


class BookState(Enum):
    Free = 0
    Dumping = 1
    Failure = 2
    Success = 3


class TableColumn(IntEnum):
    title = 0
    author = 1
    status = 2
    site = 3
    progress = 4
    log = 5
    columnCount = 6


class BookTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.__listdata = []

    def updateData(self, listdata):
        self.__listdata = listdata
        self.beginResetModel()
        self.endResetModel()

    def removeRow(self, row):
        if row >= 0 and row < len(self.__listdata):
            del self.__listdata[row]
            self.beginResetModel()
            self.endResetModel()

    def setLog(self, row, text):
        self.setData2(row, TableColumn.log, text)

    def setStatus(self, row, text):
        self.setData2(row, TableColumn.status, text)

    def setProgress(self, row, text):
        self.setData2(row, TableColumn.progress, text)

    def setState(self, row, text):
        if row >= 0 and row < self.rowCount():
            self.__listdata[row]['state'] = text

    def getState(self, row):
        if row >= 0 and row < self.rowCount():
            return self.__listdata[row]['state']
        return None

    def setSources(self, row, sources):
        if row >= 0 and row < self.rowCount():
            self.__listdata[row]['sources'] = sources
            if len(sources) > 0:
                idx = 0
                selected = 0
                for item in sources:
                    if item['selected'] == 1:
                        selected = idx
                        break
                    idx += 1
                self.setData2(row, TableColumn.site, sources[
                              selected]['site_name'])

    def getSources(self, row):
        if row >= 0 and row < self.rowCount():
            site_name = self.data2(row, TableColumn.site)
            sources = self.__listdata[row]['sources']
            if sources is not None:
                for item in sources:
                    if site_name == item['site_name']:
                        return item
        return None

    def getId(self, row):
        if row >= 0 and row < self.rowCount():
            return self.__listdata[row]['id']
        return None

    def getRowById(self, id):
        row = 0
        for item in self.__listdata:
            if item['id'] == id:
                return row
            row += 1

    def getFreeRow(self):
        for row in xrange(0, self.rowCount()):
            state = self.__listdata[row]['state']
            if state == BookState.Free:
                return row
        return -1

    def setAllState(self, oldstate, newstate):
        for item in self.__listdata:
            if item['state'] == oldstate:
                item['state'] = newstate

    def setData2(self, row, column, value, role=QtCore.Qt.EditRole):
        index = QtCore.QAbstractTableModel.index(self, row, column)
        if self.setData(index, value, role):
            self.beginResetModel()
            self.endResetModel()

    def data2(self, row, column, role=QtCore.Qt.DisplayRole):
        index = self.index(row, column)
        return self.data(index, role)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return TableColumn.columnCount

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__listdata)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == TableColumn.title:
                    return u'名称'
                if section == TableColumn.author:
                    return u'作者'
                if section == TableColumn.site:
                    return u'书源'
                if section == TableColumn.status:
                    return u'状态'
                if section == TableColumn.progress:
                    return u'进度'
                if section == TableColumn.log:
                    return u'日志'
            elif orientation == QtCore.Qt.Vertical:
                return section
        return QtCore.QVariant()

    def data(self, index, role):
        if index.isValid():
            if role == QtCore.Qt.TextColorRole:
                if self.__listdata[index.row()]['state'] == BookState.Dumping:
                    return QtGui.QColor(QtCore.Qt.blue)
                if self.__listdata[index.row()]['state'] == BookState.Success:
                    return QtGui.QColor(31, 170, 54)
                if self.__listdata[index.row()]['state'] == BookState.Failure:
                    return QtGui.QColor(QtCore.Qt.red)
            elif role == QtCore.Qt.DisplayRole:
                if index.column() == TableColumn.title:
                    return self.__listdata[index.row()]['title']
                if index.column() == TableColumn.author:
                    return self.__listdata[index.row()]['author']
                if index.column() == TableColumn.site:
                    return self.__listdata[index.row()]['site']
                if index.column() == TableColumn.status:
                    return self.__listdata[index.row()]['status']
                if index.column() == TableColumn.progress:
                    return self.__listdata[index.row()]['progress']
                if index.column() == TableColumn.log:
                    return self.__listdata[index.row()]['log']
            elif role == QtCore.Qt.EditRole:
                if index.column() == TableColumn.site:
                    return self.__listdata[index.row()]['sources']
            return QtCore.QVariant()
        return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() is False:
            return False
        if role != QtCore.Qt.EditRole:
            return False
        if index.column() == TableColumn.title:
            self.__listdata[index.row()]['title'] = value
        elif index.column() == TableColumn.author:
            self.__listdata[index.row()]['author'] = value
        elif index.column() == TableColumn.site:
            self.__listdata[index.row()]['site'] = value
        elif index.column() == TableColumn.status:
            self.__listdata[index.row()]['status'] = value
        elif index.column() == TableColumn.progress:
            self.__listdata[index.row()]['progress'] = value
        elif index.column() == TableColumn.log:
            self.__listdata[index.row()]['log'] = value
        else:
            return False
        return True

    def flags(self, index):
        if index.isValid() is False:
            return QtCore.Qt.NoItemFlags

        flag = QtCore.QAbstractItemModel.flags(self, index)
        if index.column() == TableColumn.site:
            flag |= QtCore.Qt.ItemIsEditable
        return flag
