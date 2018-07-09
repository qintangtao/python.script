#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PyQt4 import QtGui, QtCore
from enum import Enum


class BookState(Enum):
    Free = 0
    Dumping = 1
    Failure = 2
    Success = 3


class BookTableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None, *args):
        QtCore.QAbstractListModel.__init__(self, parent, *args)
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

    def setLog(self, row, log):
        if row >= 0 and row < len(self.__listdata):
            self.__listdata[row]['log'] = log
            self.beginResetModel()
            self.endResetModel()

    def setProgress(self, row, progress):
        if row >= 0 and row < len(self.__listdata):
            self.__listdata[row]['progress'] = progress
            self.beginResetModel()
            self.endResetModel()

    def setState(self, row, state):
        if row >= 0 and row < len(self.__listdata):
            self.__listdata[row]['state'] = state
            self.beginResetModel()
            self.endResetModel()

    def getState(self, row):
        if row >= 0 and row < len(self.__listdata):
            return self.__listdata[row]['state']
        return None

    def getId(self, row):
        if row >= 0 and row < len(self.__listdata):
            return self.__listdata[row]['id']
        return None

    def getFreeRow(self):
        for row in xrange(0, self.rowCount()):
            state = self.__listdata[row]['state']
            if state == BookState.Free:
                return row
        return -1

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 4

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__listdata)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section == 0:
                    return u'名称'
                if section == 1:
                    return u'作者'
                if section == 2:
                    return u'进度'
                if section == 3:
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
                if index.column() == 0:
                    return self.__listdata[index.row()]['title']
                if index.column() == 1:
                    return self.__listdata[index.row()]['author']
                if index.column() == 2:
                    return self.__listdata[index.row()]['progress']
                if index.column() == 3:
                    return self.__listdata[index.row()]['log']
            return QtCore.QVariant()
        return QtCore.QVariant()
