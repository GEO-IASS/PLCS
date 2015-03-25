# -*- coding: utf-8 -*-

# Created: Tue Jan 20 14:55:17 2015
#      by: PyQt4 UI code generator 4.10.4

from qgis import gui
from PyQt4 import QtCore, QtGui
from math import sqrt
import numpy

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

class Ui_DockWidget(object):
    def __init__(self):
        self.totalBandNumber = None

    def setupUi(self, DockWidget):
        DockWidget.setObjectName(_fromUtf8("DockWidget"))
        DockWidget.resize(255, 255)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))

        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setSpacing(2)

        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.graphicHorizontalLayoutList = []

        self.nBarSpinBox = QtGui.QSpinBox(DockWidget)
        self.nBarSpinBox.setValue(20)
        self.nBarSpinBox.setMinimum(1)
        self.nBarSpinBox.setMaximum(256)
        self.nBarSpinBox.setFixedWidth(50)
        self.nBarSpinBox.setSingleStep(5)

        self.nBarSpinBox.setObjectName(_fromUtf8("nBarSpinBox"))

        self.bandNumberComboBox = QtGui.QComboBox(DockWidget)
        self.bandNumberComboBox.setObjectName(_fromUtf8("bandNumberComboBox"))
        self.bandNumberComboBox.addItem(str(1), 1)

        self.mMapLayerComboBox = gui.QgsMapLayerComboBox(DockWidget)
        self.mMapLayerComboBox.setFilters(gui.QgsMapLayerProxyModel.RasterLayer)
        self.mMapLayerComboBox.setObjectName(_fromUtf8("mMapLayerComboBox"))
        self.mMapLayerComboBox.setFixedWidth(110)
        self.pushButton = QtGui.QPushButton(DockWidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.batch_pushButton = QtGui.QPushButton(DockWidget)
        self.batch_pushButton.setObjectName(_fromUtf8("batch_pushButton"))
        self.batch_pushButton.setFixedWidth(60)
        self.save_pushButton = QtGui.QPushButton(DockWidget)
        self.save_pushButton.setObjectName(_fromUtf8("save_pushButton"))
        self.load_pushButton = QtGui.QPushButton(DockWidget)
        self.load_pushButton.setObjectName(_fromUtf8("load_pushButton"))
        self.auto_pushButton = QtGui.QPushButton(DockWidget)
        self.auto_pushButton.setObjectName(_fromUtf8("auto_pushButton"))
        self.auto_pushButton.setFixedWidth(60)
        self.help_pushButton = QtGui.QPushButton(DockWidget)
        self.help_pushButton.setObjectName(_fromUtf8("help_pushButton"))
        self.help_pushButton.setFixedWidth(60)
        
        self.horizontalLayout.addWidget(self.mMapLayerComboBox)
        self.horizontalLayout.addWidget(self.nBarSpinBox)
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addWidget(self.bandNumberComboBox)
        self.horizontalLayout_2.addWidget(self.batch_pushButton)
        self.horizontalLayout_2.addWidget(self.save_pushButton)
        self.horizontalLayout_2.addWidget(self.load_pushButton)
        self.horizontalLayout_2.addWidget(self.auto_pushButton)
        self.verticalLayout.addWidget(self.help_pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.verticalLayoutGraphics = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayoutGraphics.setObjectName(_fromUtf8("verticalLayout"))

        self.graphicsViewPreview = QtGui.QGraphicsView(DockWidget)
        self.graphicsViewPreview.setObjectName(_fromUtf8("graphicsViewPreview"))
        self.scenePreview = QtGui.QGraphicsScene()
        self.graphicsViewPreview.setScene(self.scenePreview);
        self.graphicsViewPreview.setFixedHeight(160)
        self.graphicsViewPreview.setFixedWidth(160)

        self.retranslateUi(DockWidget)

        self.graphicsViewPreview.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff);
        self.graphicsViewPreview.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff);

        spacerItem = QtGui.QSpacerItem(20, 100, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.graphicsViewPreview)
        self.verticalLayout.addItem(spacerItem)

        self.changeContent(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def changeContent(self, DockWidget):
        DockWidget.setWidget(self.dockWidgetContents)
        
    def resetBandNumber(self, maxBandNumber, totalBandNumber):
        self.totalBandNumber = totalBandNumber
        if maxBandNumber == 3 :
            if self.bandNumberComboBox.count() == 1:
                self.bandNumberComboBox.addItem(str(3), 3)
        else:
            if self.bandNumberComboBox.count() == 2:
                self.bandNumberComboBox.removeItem(1)

        
    def changeBandNumber(self, DockWidget, bandNumber):
        for i, layout in enumerate(self.graphicHorizontalLayoutList):
            layout.removeWidget(self.graphicList[i])
            self.graphicList[i].hide()
            layout.removeWidget(self.bandComboboxList[i])
            self.bandComboboxList[i].hide()
        self.graphicList = []
        self.sceneList = []
        self.bandComboboxList = []
        self.graphicHorizontalLayoutList = []

        for i in range(bandNumber):
            graphicsView = customView(DockWidget)
            graphicsView.setObjectName(_fromUtf8("graphicsView"))
            graphicsView.getSpinValue = self.nBarSpinBox.value
            graphicsView.setFixedHeight(100)
            graphicsView.setFixedWidth(255)
            graphicsView.setSceneRect(QtCore.QRectF(-255, -255, 510, 510))
            graphicsView.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff);
            graphicsView.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff);
            scene = customScene()
            graphicsView.setScene(scene)
            node = QGNode(0, 0, 6)
            self.graphicList.append(graphicsView)
            scene.addNode(node)
            self.sceneList.append(scene)
            
            bandCombobox = QtGui.QComboBox(DockWidget)
            for j in range(1, self.totalBandNumber + 1):
                bandCombobox.addItem(str(j), j)
            bandCombobox.setCurrentIndex(i)
            bandCombobox.setFixedWidth(40)
            self.bandComboboxList.append(bandCombobox)
            horizontalLayoutGraphic = QtGui.QHBoxLayout(self.dockWidgetContents)
            horizontalLayoutGraphic.setObjectName(_fromUtf8("horizontalLayoutGraphic"))
            horizontalLayoutGraphic.addWidget(graphicsView)
            horizontalLayoutGraphic.addWidget(bandCombobox)
            self.graphicHorizontalLayoutList.append(horizontalLayoutGraphic)
            self.verticalLayout.insertLayout(3, horizontalLayoutGraphic)

    def reinit(self, dataList):
        for scene in self.sceneList:
            items = scene.items()
            for item in items:
                scene.removeItem(item)
            node = QGNode(0, 0, 6)
            scene.addNode(node)

        for graphic, dataC in zip(self.graphicList, dataList):
            graphic.setData(dataC)
            graphic.drawHistogram(dataC)
            
    def setNodes(self, nodeArray):
        for scene, nodeList in zip(self.sceneList, nodeArray):
            items = scene.items()
            for item in items:
                scene.removeItem(item)
            for node in nodeList:
                node = QGNode(node[0], node[1], 6)
                scene.addNode(node)

        for graphic in self.graphicList:
            graphic.refreshBreakList()
            graphic.refreshLine()
            graphic.resetHistograms()

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(_translate("DockWidget", "Piecewise Linear Stretched Histogram", None))
        self.pushButton.setText(_translate("DockWidget", "Transform", None))
        self.batch_pushButton.setText(_translate("DockWidget", "Batch", None))
        self.save_pushButton.setText(_translate("DockWidget", "Save breaks", None))
        self.load_pushButton.setText(_translate("DockWidget", "Load breaks", None))
        self.auto_pushButton.setText(_translate("DockWidget", "Auto", None))
        self.help_pushButton.setText(_translate("DockWidget", "Help", None))


class customScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)
        
    def addNode(self, node):
        self.addItem(node)


class customView(QtGui.QGraphicsView):
    refreshSignal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtGui.QGraphicsView.__init__(self, parent)

        self.breakList = []
        self.currentBoundary = []
        self.data = None
        self.alpha = None
        
    def setData(self, data):
        self.data = data

    def mousePressEvent(self, ev):
        self.refreshBreakList()
        self._start = ev.pos()
        if QtCore.Qt.RightButton == ev.button():
            painter = QtGui.QPainterPath();
            point = self.mapToScene(ev.pos())
            x = point.x()
            y = point.y()
            if self.isAreaValidForNewBreak(x, y):
                painter.addEllipse(x, y, 20, 20)
                self.scene().setSelectionArea(painter)
                if self.scene().selectedItems() != []:
                    if len(self.breakList) < 2:
                        return
                    for item in self.scene().selectedItems():
                        self.scene().removeItem(item)
                        return
                else:
                    self.scene().addNode(QGNode(x, y, 6))

        QtGui.QGraphicsView.mousePressEvent(self, ev)
        self.refreshBreakList()
        self.refreshLine()

        if self.scene().selectedItems() is not None and self.scene().selectedItems() != []:
            selectedBreakPoint = self.scene().selectedItems()[0]
            self.currentBoundary = [0, 0, 0, 0]
            index = -1
            for breakPoint in self.breakList:
                index += 1
                if selectedBreakPoint == breakPoint:
                    currentIndex = index
                    break
            self.currentIndex = index
            if currentIndex == 0:
                self.currentBoundary[0] = -self.viewport().width() / 2
                self.currentBoundary[1] = self.viewport().height() / 2
            else:
                self.currentBoundary[0] = self.breakList[index - 1].rect().center().x() + self.breakList[index - 1].pos().x()
                self.currentBoundary[1] = self.breakList[index - 1].rect().center().y() + self.breakList[index - 1].pos().y()
            if currentIndex == (len(self.breakList) - 1):
                self.currentBoundary[2] = self.viewport().width() / 2
                self.currentBoundary[3] = -self.viewport().height() / 2
            else:
                self.currentBoundary[2] = self.breakList[index + 1].rect().center().x() + self.breakList[index + 1].pos().x()
                self.currentBoundary[3] = self.breakList[index + 1].rect().center().y() + self.breakList[index + 1].pos().y()

    def mouseMoveEvent(self, ev):
        QtCore.QCoreApplication.processEvents()
        if self.currentBoundary != [] and self.scene().selectedItems() != [] :
            selectedBreakPoint = self.breakList[self.currentIndex]
            pos = selectedBreakPoint.rect().center() + selectedBreakPoint.pos()
            x = pos.x()
            y = pos.y()
            deltax = -self._start.x() + ev.pos().x()
            deltay = -self._start.y() + ev.pos().y()

            if x > self.currentBoundary[0] + 1  or deltax > 0:
                if y < self.currentBoundary[1] - 1  or deltay < 0:
                    if x < self.currentBoundary[2] - 1  or deltax < 0:
                        if y > self.currentBoundary[3] + 1  or deltay > 0:
                            QtGui.QGraphicsView.mouseMoveEvent(self, ev)
                            self.refreshLine()

    def mouseReleaseEvent(self, ev):
        QtGui.QGraphicsView.mouseReleaseEvent(self, ev)
        self.scene().clearSelection()
        self.refreshBreakList()
        self.refreshLine()
        self.resetHistograms()
        self.refreshSignal.emit()
        
    def changeHistogramBarNumber(self):
        if self.data is not None:
            self.setAlpha()
            self.resetHistograms()

    def resetHistograms(self):
        poly = self.items()
        poly = [x for x in poly if isinstance(x, QtGui.QGraphicsPolygonItem)]
        for i in range(len(poly)):
            self.scene().removeItem(poly[i])
        if self.data is not None:
            self.drawHistogram(self.data)
            self.redrawNewHistogram()
        
    def refreshLine(self):
        Lines = self.items()
        Line = [x for x in Lines if isinstance(x, QtGui.QGraphicsLineItem)]
        for i in range(len(Line)):
            self.scene().removeItem(Line[i])

        start = QtCore.QPoint(-self.viewport().width() / 2, self.viewport().height() / 2)
        end = self.breakList[0].rect().center() + self.breakList[0].pos()
        self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))

        for i in range(len(self.breakList) - 1):
            start = self.breakList[i].rect().center() + self.breakList[i].pos()
            end = self.breakList[i + 1].rect().center() + self.breakList[i + 1].pos()
            self.scene().addItem(
                QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))

        start = self.breakList[-1].rect().center() + self.breakList[-1].pos()
        end = QtCore.QPoint(self.viewport().width() / 2, -self.viewport().height() / 2)
        self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))


    def redrawNewHistogram(self):
        newData = self.transformData(self.data)
        newBrush = QtGui.QBrush(QtGui.QColor(255, 170, 0, 50))
        self.drawHistogram(newData, newBrush)
        
    def transformData(self, data):
        X = [0]
        Y = [0]
        for breakPoint in self.breakList:
            point = breakPoint.rect().center() + breakPoint.pos()
            X.append((point.x() + 255 / 2.0))
            Y.append((-point.y() / self.size().height() * 255 + 255 / 2.0))
        X.append(255)
        Y.append(255)
        newdata = []
        for dat in numpy.nditer(data):
            if dat == 0.0:
                newdata.append(0)
                continue
            i = 1
            while (dat > X[i]):
                i += 1
            else:
                newdata.append((Y[i - 1] + float(Y[i] - Y[i - 1]) / (X[i] - X[i - 1]) * float(dat - X[i - 1])))
        newdataAsArray = numpy.array(newdata, dtype=numpy.float64)
        newdataAsArray = newdataAsArray.reshape(data.shape)
        return newdataAsArray
        
    def drawHistogram(self, data, cbrush=None):
        if self.alpha is None:
            self.setAlpha()
        if cbrush is None:
            cbrush = QtGui.QBrush(QtGui.QColor(10, 100, 255, 50))
        hr = numpy.histogram(data, self.getSpinValue(), range=(0, 255))
        countInClasses = hr[0]
        classes = list(hr[1])
        sw = self.size().width()
        sh = self.size().height()
        for i, count in enumerate(countInClasses):
            polygon = QtGui.QPolygon([QtCore.QPoint((classes[i] * sw / 255) - sw / 2, sh / 2),
                                      QtCore.QPoint((classes[i] * sw / 255) - sw / 2, (-count * self.alpha + sh / 2)) ,
                                      QtCore.QPoint((classes[i + 1] * sw / 255) - sw / 2, (-count * self.alpha + sh / 2)),
                                      QtCore.QPoint((classes[i + 1] * sw / 255) - sw / 2, sh / 2) ])
            self.scene().addPolygon(QtGui.QPolygonF(polygon), brush=cbrush)

    def setAlpha(self):
        hr = numpy.histogram(self.data, self.getSpinValue(), range=(0, 255))
        countInClasses = hr[0]
        maxCount = max(countInClasses)
        self.alpha = self.size().height() / float(2 * maxCount)
        
            
    def isAreaValidForNewBreak(self, x1, y1):
        items = self.items()
        items = [x for x in items if isinstance(x, QGNode)]
        for i in range(len(items)):
            pos0 = items[i].rect().center() + items[i].pos()
            x0 = pos0.x(); y0 = pos0.y()
            if x1 >= x0:
                if y1 <= y0:
                    pass
                else:
                    return False
            else:
                if y1 >= y0:
                    pass
                else:
                    return False
        return True
    
    def refreshBreakList(self):
        items = self.items()
        items = [x for x in items if isinstance(x, QGNode)]
        self.breakList = []
        for i in range(len(items)):
            pos1 = items[i].rect().center() + items[i].pos()
            x1 = pos1.x(); y1 = pos1.y()
            index = 0
            for breakPoint in self.breakList:
                pos0 = breakPoint.rect().center() + breakPoint.pos()
                x0 = pos0.x(); y0 = pos0.y();
                if x1 >= x0:
                    if y1 <= y0:
                        index += 1
            self.breakList.insert(index, items[i])

    def scrollContentsBy(self, dx, dy):
        return

class QGNode(QtGui.QGraphicsEllipseItem):
    def __init__(self, x, y, r, parent=None):
        QtGui.QGraphicsEllipseItem.__init__(self, parent)

        QtGui.QGraphicsEllipseItem.__init__(self, x - r, y - r, 2 * r, 2 * r)
        self.setBrush(QtCore.Qt.black)

        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setZValue(10)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(QtCore.Qt.yellow)
        QtGui.QGraphicsEllipseItem.hoverEnterEvent(self, event)

    def mousePressEvent(self, event):
        self.setBrush(QtCore.Qt.cyan)
        QtGui.QGraphicsEllipseItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.setBrush(QtCore.Qt.green)
        QtGui.QGraphicsEllipseItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setBrush(QtCore.Qt.blue)
        QtGui.QGraphicsEllipseItem.mouseReleaseEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QtCore.Qt.black)
        QtGui.QGraphicsEllipseItem.hoverLeaveEvent(self, event)

