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
from qgis.gui import QgsMessageBar
from PyQt4 import QtGui, QtCore, QtXml

from ..uis.ui_mainDock import Ui_DockWidget
from batch_widget import BatchDialog

import numpy
from numpy import max, min
from osgeo import gdal
from osgeo.gdalnumeric import *
from osgeo.gdalconst import *
import Image

from lxml import etree
from numpy import histogram, uint8, random
from os import listdir
from functools import partial


class mainDockWidget(QtGui.QDockWidget):
    def __init__(self, iface, parent=None):
        QtGui.QDockWidget.__init__(self)
        self.ui = Ui_DockWidget()
        self.ui.setupUi(self)
        self.imageList = None
        self.iface = iface
        self.dataprList = None

        self.ui.pushButton.released.connect(self.transform)
        self.ui.mMapLayerComboBox.setLayer(None)
        self.ui.mMapLayerComboBox.layerChanged.connect(self.layerChanged)
        self.ui.bandNumberComboBox.currentIndexChanged.connect(self.displayBandNumberChanged)
        
    @QtCore.pyqtSlot()
    def on_batch_pushButton_released(self):
        if not self.layerIsDefined():
            return

        self.batchDialog = BatchDialog()
        self.batchDialog.exec_()
        folder = self.batchDialog.ui.lineEdit.text()
        if not self.batchDialog.command:
            return
        if os.path.isdir(folder):
            return

        f = []
        for file in listdir(folder):
            if (file.endswith('.tif')
                or file.endswith('.tiff')
                or file.endswith('.TIF')
                or file.endswith('.TIFF')):
                f.append(file)
        for file in f:
            self.transform(file, folder)
        
    def layerChanged(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        if not self.layerIsDefined():
            return
        layer = self.ui.mMapLayerComboBox.currentLayer()
        b = max([1, min([3, layer.bandCount()])])

        self.ui.resetBandNumber(b, layer.bandCount())
        self.getData(layer)
        cI = self.ui.bandNumberComboBox.currentIndex()
        if cI == floor(b / 2.0):
            self.displayBandNumberChanged()
        else:
            self.ui.bandNumberComboBox.setCurrentIndex(floor(b / 2.0))
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

    def displayBandNumberChanged(self):
        if not self.layerIsDefined() or self.dataprList is None:
            return
        self.ui.changeBandNumber(self,
                                 self.ui.bandNumberComboBox.itemData(
                                            self.ui.bandNumberComboBox.currentIndex()))
        self.ui.changeContent(self)
        for cb, graphic in zip(self.ui.bandComboboxList, self.ui.graphicList):
            self.ui.nBarSpinBox.valueChanged.connect(graphic.changeHistogramBarNumber)
            cb.currentIndexChanged.connect(partial(
                                                self.refreshDataInHistogram,
                                                graphic, cb))
            graphic.refreshSignal.connect(self.updatePreview)
        dataList = []
        for i, graphic in enumerate(self.ui.graphicList):
            dataList.append(self.dataprList[self.ui.bandComboboxList[i].itemData(self.ui.bandComboboxList[i].currentIndex()) - 1])
        self.ui.reinit(dataList)
        self.updatePreview()
        
    def refreshDataInHistogram(self, graphic, combobox):
        if not self.layerIsDefined():
            return
        dataC = self.dataprList[combobox.itemData(combobox.currentIndex()) - 1]
        graphic.setData(dataC)
        graphic.resetHistograms()
        self.updatePreview()
            
    def getData(self, layer):
        # Open the dataset
        ds1 = gdal.Open(layer.publicSource(), GA_ReadOnly)
        self.imageList = []
        self.dataprList = []
        for i in range(0, layer.bandCount()):
            band = ds1.GetRasterBand(i + 1)

            # Read the data into numpy arrays
            data = BandReadAsArray(band)
            self.imageList.append(self.arrayToImage(data[0::10, 0::10]))

            # The actual calculation
            self.dataprList.append(numpy.random.choice(data[data[:] > 0], 1000))
            band = None
            data = None
        
    def currentCBIndex(self, index):
        return self.ui.bandComboboxList[index].itemData(
                        self.ui.bandComboboxList[index].currentIndex()) - 1;

    def updatePreview(self):
        if self.imageList is None:
            return
        self.ui.scenePreview.clear()
        h = self.imageList[0].size[0]
        w = self.imageList[0].size[1]
        bgra = empty((w, h, 4), numpy.uint8, 'C')

        if self.ui.bandNumberComboBox.itemData(self.ui.bandNumberComboBox.currentIndex()) > 1:
            dataOutList = []
            for i, graphic in enumerate(self.ui.graphicList):
                im = self.imageList[self.currentCBIndex(i)]
                NewLUT = graphic.transformData(array(range(256)))
                dataOut = self.imageToArray(im.point(NewLUT))
                dataOutList.append(array(dataOut, dtype=uint32))
            bgra[..., 0] = dataOutList[2]
            bgra[..., 1] = dataOutList[1]
            bgra[..., 2] = dataOutList[0]

        else:
            NewLUT = self.ui.graphicList[0].transformData(array(range(256)))
            dataOut = self.imageToArray(self.imageList[self.currentCBIndex(0)].point(NewLUT))
            dataOut = array(dataOut, dtype=uint32)
            bgra[..., 0] = dataOut
            bgra[..., 1] = dataOut
            bgra[..., 2] = dataOut

        bgra[..., 3].fill(255)
        fmt = QtGui.QImage.Format_RGB32
        dataOut1, dataOut2, dataOut3 = None, None, None
        im = QtGui.QImage(bgra, h, w, fmt)
        preview = QtGui.QPixmap.fromImage(im)
        preview = preview.scaled(QtCore.QSize(150, 150), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.ui.scenePreview.addPixmap(preview)
        self.ui.scenePreview.update()
        
    def transform(self, inputFile=None, folder=None):
        if not self.layerIsDefined():
            return
        if inputFile is None:
            layer = self.ui.mMapLayerComboBox.currentLayer()
            fileName = layer.publicSource()
            outFile = QtGui.QFileDialog.getSaveFileName(self, "Save File",
                                "",
                                "Images (*.tiff *.TIFF *.tif, *.TIF)")
            if outFile is None or outFile == '':
                return
            if (outFile.endswith('.tif')
                or outFile.endswith('.tiff')
                or outFile.endswith('.TIF')
                or outFile.endswith('.TIFF')):
                pass
            else:
                outFile = outFile + '.tiff'
            layer = self.ui.mMapLayerComboBox.currentLayer()
            fileName = layer.publicSource()
        # If inputFile name is give:
        else:
            fileName = folder + '/' + inputFile
            inputFileSplitted = inputFile.split('.')
            outFile = folder + '/' + inputFileSplitted[0] + '_PLHS.' + inputFileSplitted[1]
            
        # Open the dataset
        ds1 = gdal.Open(fileName, GA_ReadOnly)

        if self.ui.bandNumberComboBox.itemData(self.ui.bandNumberComboBox.currentIndex()) > 1\
            and ds1.RasterCount > 1:
            bandNum1 = self.currentCBIndex(0) + 1
            bandNum2 = self.currentCBIndex(1) + 1
            bandNum3 = self.currentCBIndex(2) + 1
            band1 = ds1.GetRasterBand(bandNum1)
            band2 = ds1.GetRasterBand(bandNum2)
            band3 = ds1.GetRasterBand(bandNum3)
            # Read the data into numpy arrays
            data1 = BandReadAsArray(band1)
            data2 = BandReadAsArray(band2)
            data3 = BandReadAsArray(band3)
            dataType = band1.DataType
            dtype = data1.dtype
            if dtype != 'uint8':
                QtGui.QMessageBox.critical(self, "Input - error",
                                           u"le fichier d'entrer n'est pas 8bits")
                return

            im1 = self.arrayToImage(data1)
            im2 = self.arrayToImage(data2)
            im3 = self.arrayToImage(data3)
            NewLUT1 = self.ui.graphicList[0].transformData(array(range(256)))
            NewLUT2 = self.ui.graphicList[1].transformData(array(range(256)))
            NewLUT3 = self.ui.graphicList[2].transformData(array(range(256)))
            dataOut1 = self.imageToArray(im1.point(NewLUT1))
            dataOut2 = self.imageToArray(im2.point(NewLUT2))
            dataOut3 = self.imageToArray(im3.point(NewLUT3))
            im1 = None
            im2 = None
            im3 = None

            dataOut1 = array(dataOut1, dtype=dtype)
            dataOut2 = array(dataOut2, dtype=dtype)
            dataOut3 = array(dataOut3, dtype=dtype)
            # Write the out file
            driver = gdal.GetDriverByName("GTiff")
            dsOut = driver.Create(outFile, ds1.RasterXSize, ds1.RasterYSize, 3, gdal.GDT_Byte)
            CopyDatasetInfo(ds1, dsOut)
            bandOut1 = dsOut.GetRasterBand(1)
            bandOut2 = dsOut.GetRasterBand(2)
            bandOut3 = dsOut.GetRasterBand(3)
            BandWriteArray(bandOut1, dataOut1)
            BandWriteArray(bandOut2, dataOut2)
            BandWriteArray(bandOut3, dataOut3)

            # Close the datasets
            band1 = None
            band2 = None
            band3 = None
            ds1 = None
            bandOut1 = None
            bandOut2 = None
            bandOut3 = None
            dsOut = None
            """
            src_ds = gdal.Open(outFile)
            dst_ds = driver.CreateCopy("/home/gmilani/PLSH_compress.tiff",
                                        src_ds,
                                        0,
                                        ['COMPRESS=LZW' ])

            # Once we're done, close properly the dataset
            dst_ds = None
            src_ds = None
            """
            fileInfo = QtCore.QFileInfo(outFile)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(outFile, baseName)
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)
        else:
            bandNum1 = self.currentCBIndex(0) + 1
            band1 = ds1.GetRasterBand(bandNum1)
            # Read the data into numpy arrays
            data1 = BandReadAsArray(band1)
            dataType = band1.DataType
            dtype = data1.dtype

            if dtype != 'uint8':
                QtGui.QMessageBox.critical(self, "Input - error",
                                           u"le fichier d'entrer n'est pas 8bits")
                return

            im1 = self.arrayToImage(data1)
            NewLUT1 = self.ui.graphicList[0].transformData(array(range(256)))
            dataOut1 = self.imageToArray(im1.point(NewLUT1))
            im1 = None

            dataOut1 = array(dataOut1, dtype=dtype)
            # Write the out file
            driver = gdal.GetDriverByName("GTiff")
            dsOut = driver.Create(outFile, ds1.RasterXSize, ds1.RasterYSize, 1, gdal.GDT_Byte)
            CopyDatasetInfo(ds1, dsOut)
            bandOut1 = dsOut.GetRasterBand(1)
            BandWriteArray(bandOut1, dataOut1)

            # Close the datasets
            band1 = None
            ds1 = None
            bandOut1 = None
            dsOut = None
            """
            src_ds = gdal.Open(outFile)
            dst_ds = driver.CreateCopy("/home/gmilani/PLSH_compress.tiff",
                                        src_ds,
                                        0,
                                        ['COMPRESS=LZW' ])

            # Once we're done, close properly the dataset
            dst_ds = None
            src_ds = None
            """
            fileInfo = QtCore.QFileInfo(outFile)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(outFile, baseName)
            QgsMapLayerRegistry.instance().addMapLayer(rlayer)

    def arrayToImage(self, a):
        """
        Converts a gdalnumeric array to a
        Python Imaging Library Image.
        """
        i=Image.fromstring('L',(a.shape[1],a.shape[0]),
                (a.astype('b')).tostring())
        return i

    def imageToArray(self, i):
        """
        Converts a Python Imaging Library array to a
        gdalnumeric image.
        """
        a = fromstring(i.tostring(), 'b')
        a.shape = i.im.size[1], i.im.size[0]
        return a
    
    @QtCore.pyqtSlot()
    def on_auto_pushButton_released(self):
        if not self.layerIsDefined():
            return
        nodeArray = []
        for index, graphic in enumerate(self.ui.graphicList):
            data0 = self.dataprList[self.currentCBIndex(index)]
            hr = numpy.histogram(data0, self.ui.nBarSpinBox.value(), range=(0, 255))
            countInClasses = hr[0]
            nodes = []
            sumx = 0
            for i, count in enumerate(countInClasses):
                j = 255.0 / len(countInClasses) * (i + 1)
                deltax = 255.0 * count / len(data0)
                sumx += deltax
                nodes.append([(j - 127.5), (50 - sumx / 255.0 * 100)])
            nodeArray.append(nodes)
        self.ui.setNodes(nodeArray)
        self.updatePreview()

    @QtCore.pyqtSlot()
    def on_save_pushButton_released(self):
        if not self.layerIsDefined():
            return
        fName = QtGui.QFileDialog.getSaveFileName(self, "save file dialog" , "", "config files (*.xml)");
        if fName:
            root = etree.Element("config")
            root.set("name", "data for PLHS plugin")
            for i, graphic in enumerate(self.ui.graphicList):
                layer = etree.SubElement(root, "layer")
                layer.set("layerID", unicode(i))
                layer.set("layerBand", unicode(i))
                for item in graphic.breakList:
                    pos1 = item.rect().center() + item.pos()
                    pointElmt = etree.SubElement(layer, "point")
                    xElmt = etree.SubElement(pointElmt, "x")
                    xElmt.text = str(pos1.x())
                    yElmt = etree.SubElement(pointElmt, "y")
                    yElmt.text = str(pos1.y())
            f = etree.ElementTree(root)
            f.write(fName, pretty_print=True)
    
    @QtCore.pyqtSlot()
    def on_load_pushButton_released(self):
        if not self.layerIsDefined():
            return
        configFile = QtGui.QFileDialog.getOpenFileName(self, "Open file" , "", "config files (*.xml)");
        if configFile is None or configFile == '':
            return
        else:
            file = QtCore.QFile(configFile)
            if (not file.open(QtCore.QIODevice.ReadOnly | QtCore. QIODevice.Text)):
                QtGui.QMessageBox.warning(QtGui.QDialog(), 'Application',
                                          "Cannot read file %s :\n%s."
                                          % (file.fileName(), file.errorString()))
                return False
            else:
                doc = QtXml.QDomDocument("EnvironmentML")
                if(not doc.setContent(file)):
                    file.close()
                    QMessageBox.warning(
                        self, "Error", "Could not parse xml file.")
                file.close()
                root = doc.documentElement()
                if(root.tagName() != "config"):
                    QMessageBox.warning(
                        self, "Error", "Could not parse xml file. Root Element must be <kml/>.")
                else:
                    t = self.getNodes(root)
                    if len(t) == 3:
                        self.ui.bandNumberComboBox.setCurrentIndex(1)
                    elif len(t) == 1:
                        self.ui.bandNumberComboBox.setCurrentIndex(0)
                    else:
                        return # must raise error instead
                    nodeArray = []
                    for list in t:
                        nodeList = []
                        lc = list[1]
                        for node in lc:
                            n = node[1]
                            nodeList.append([float(n[0][1]), float(n[1][1])])
                        nodeArray.append(nodeList)
                    self.ui.setNodes(nodeArray)


    def getNodes(self, node, parent=None):
        if parent == 'x' or parent == 'y' :
            text = node.firstChild().toText().data()
        else:
            text = []
            n = node.firstChild()
            while (not n.isNull()):
                t = n.nodeName()
                if n.nodeType() == 1:
                    rec = self.getNodes(n, t)
                    if n.toElement().hasAttribute('layerID'):
                        id = n.toElement().attribute('layerID')
                        band = n.toElement().attribute('layerBand')
                        group = [t, rec, id, band]
                    else:
                        group = [t, rec]
                    text.append(group)
                n = n.nextSibling()
        return text

    def layerIsDefined(self):
        if self.ui.mMapLayerComboBox.currentLayer() is None:
            self.iface.messageBar().pushMessage(u"PLHS",
                                     u"No layer selected",
                                     QgsMessageBar.WARNING, 5)
            return False
        else:
            return True
