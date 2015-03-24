# -*- coding: utf-8 -*-
"""
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsRasterLayer, QgsMapLayerRegistry
from PyQt4 import QtGui, QtCore
from ..uis.batch_ui import Ui_Batch


class BatchDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Batch()
        self.ui.setupUi(self)
        self.command = False
            
    @QtCore.pyqtSlot()
    def on_toolButton_released(self):
        file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file is None or file == '':
            return
        else:
            self.ui.lineEdit.setText(file)

    @QtCore.pyqtSlot()
    def on_commandLinkButton_released(self):
        self.command = True
        self.close()



