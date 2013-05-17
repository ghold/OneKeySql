from PyQt4 import QtGui, QtCore, Qt
from OkListItem import OkListItem
from OkScrollBar import OkScrollBar
from PyQt4.QtCore import pyqtSlot

class OkListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setSelectionMode(3)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMinimumWidth(250)
        self.setVerticalScrollBar(OkScrollBar())
        self.setSpacing(1)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setMouseTracking(True)
        
class OkCaseWidget(OkListWidget):
    def __init__(self, parent=None):
        OkListWidget.__init__(self, parent)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
        
    @pyqtSlot(OkListItem)
    def pressItem(self, item):
        itemdata = repr(item.data(Qt.Qt.UserRole))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text())
        mimeData.setData('application/x-dict', itemdata.encode("utf-8"))
        
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
            
class OkUnitWidget(OkListWidget):
    def __init__(self, parent=None):
        OkListWidget.__init__(self, parent)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dict'):
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    @pyqtSlot(OkListItem)
    def pressItem(self, item):
        itemdata = repr(item.data(Qt.Qt.UserRole))
        print(itemdata.encode("utf-8"))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text())
        mimeData.setData('application/x-dict', itemdata.encode("utf-8"))

        pixmap = QtGui.QPixmap(item.sizeHint())
        self.render(pixmap)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()
