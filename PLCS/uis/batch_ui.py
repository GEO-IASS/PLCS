# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batch_ui.ui'
#
# Created: Mon Mar  9 15:29:01 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Batch(object):
    def setupUi(self, Batch):
        Batch.setObjectName(_fromUtf8("Batch"))
        Batch.resize(349, 86)
        self.gridLayout = QtGui.QGridLayout(Batch)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Batch)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(Batch)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.toolButton = QtGui.QToolButton(Batch)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout.addWidget(self.toolButton, 0, 2, 1, 1)
        self.commandLinkButton = QtGui.QCommandLinkButton(Batch)
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.gridLayout.addWidget(self.commandLinkButton, 1, 0, 1, 3)

        self.retranslateUi(Batch)
        QtCore.QMetaObject.connectSlotsByName(Batch)

    def retranslateUi(self, Batch):
        Batch.setWindowTitle(_translate("Batch", "Batch transformation", None))
        self.label.setText(_translate("Batch", "Folder", None))
        self.toolButton.setText(_translate("Batch", "...", None))
        self.commandLinkButton.setText(_translate("Batch", "Transform whole folder with current data", None))

