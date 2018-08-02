#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PyQt4 import QtGui, QtCore


class BookItemDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None, *args):
        QtGui.QStyledItemDelegate.__init__(self, parent, *args)

    def paint(self, painter, option, index):
        opt = QtGui.QStyleOptionViewItem(option)
        if opt.state & QtGui.QStyle.State_HasFocus:
            opt.state ^= QtGui.QStyle.State_HasFocus
        QtGui.QStyledItemDelegate.paint(self, painter, opt, index)

    def createEditor(self, parent, option, index):
        sources = index.model().data(index, QtCore.Qt.EditRole)
        if sources is not None:
            editor = QtGui.QComboBox(parent)
            for item in sources:
                editor.addItem(item['site_name'])
            return editor
        return None

    def setEditorData(self, editor, index):
        site_name = index.model().data(index, QtCore.Qt.DisplayRole)
        idx = editor.findText(site_name)
        editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
