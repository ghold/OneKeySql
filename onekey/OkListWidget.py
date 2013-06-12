from PyQt4 import QtGui, QtCore, Qt
from OkListItem import OkListItem
from OkScroll import OkScrollBar

from PyQt4.QtCore import pyqtSlot

class OkListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.selectedItem = None
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setSelectionMode(0)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMinimumWidth(250)
        self.setVerticalScrollBar(OkScrollBar())
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        #self.setMouseTracking(True)
        
    @pyqtSlot(str)        
    def search(self, text):
        for i in range(self.count()):
            self.setItemHidden(self.item(i), True)
        itemList = self.findItems(text, Qt.Qt.MatchContains)
        for item in itemList:
            self.setItemHidden(item, False)
        
class OkCaseWidget(OkListWidget):
    def __init__(self, parent=None):
        OkListWidget.__init__(self, parent)
        self.setAcceptDrops(False)
        self.infoWidget = None
        self.editState = False
        
    def setOkInfo(self, widget):
        self.infoWidget = widget
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/ok-case'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/ok-case'):
            event.setDropAction(Qt.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        
    @pyqtSlot(OkListItem)
    def pressItem(self, item):
        self.topLevelWidget().basket.show()
        
        itemdata = repr(item.data(Qt.Qt.UserRole))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text())
        if item == self.selectedItem:
            id = item.data(Qt.Qt.UserRole)['id']
            row = item.listWidget().row(item)
            mimeData.setData('application/ok-case', '{"id":"%s","row":"%d"}'%(id, row))
        
        itemIndex = self.indexFromItem(item)
        itemRect = self.visualRect(itemIndex)
        pixmap = QtGui.QPixmap(itemRect.size())
        self.render(pixmap, QtCore.QPoint(0, 0), QtGui.QRegion(itemRect))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)
        self.topLevelWidget().basket.hide()

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()
        
class OkStepWidget(OkListWidget):
    def __init__(self, item, parent=None):
        OkListWidget.__init__(self, parent)
        self.item = item
        
        image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
        image.fill(QtGui.QColor(221, 221, 221))
        image.setPixel(0, 39, QtGui.qRgba(33, 133, 197, 255))
        image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
        brush = QtGui.QBrush()
        brush.setTextureImage(image)
        
        self.setStyleSheet("OkStepWidget::item:hover{"
                "background: #4da6ea;"
                "color: #fff"
            "}")
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/ok-unit'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/ok-unit'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/ok-unit'):
            event.setDropAction(QtCore.Qt.CopyAction)
            data = eval(bytes(event.mimeData().data('application/ok-unit')).decode("utf-8"))
            self.topLevelWidget().showCaseEditPad(self.item, data)
            event.accept()
        else:
            event.ignore()
            
    @pyqtSlot(OkListItem)
    def pressItem(self, item):
        self.topLevelWidget().basket.show()
        itemdata = repr(item.data(Qt.Qt.UserRole))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text())
        mimeData.setData('application/ok-step', itemdata.encode("utf-8"))

        itemIndex = self.indexFromItem(item)
        itemRect = self.visualRect(itemIndex)
        pixmap = QtGui.QPixmap(itemRect.size())
        self.render(pixmap, QtCore.QPoint(0, 0), QtGui.QRegion(itemRect))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)
        self.topLevelWidget().basket.hide()

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()
        
class OkUnitWidget(OkListWidget):
    def __init__(self, parent=None):
        OkListWidget.__init__(self, parent)
        self.setAcceptDrops(False)
        
        self.setStyleSheet("OkUnitWidget::item:hover{"
                "background: #4da6ea;"
                "color: #fff"
            "}")
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/ok-unit'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/ok-unit'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
            
    @pyqtSlot(OkListItem)
    def pressItem(self, item):
        itemdata = repr(item.data(Qt.Qt.UserRole))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text())
        mimeData.setData('application/ok-unit', itemdata.encode("utf-8"))

        itemIndex = self.indexFromItem(item)
        itemRect = self.visualRect(itemIndex)
        pixmap = QtGui.QPixmap(itemRect.size())
        self.render(pixmap, QtCore.QPoint(0, 0), QtGui.QRegion(itemRect))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()
            
