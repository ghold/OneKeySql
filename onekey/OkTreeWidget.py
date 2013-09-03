from PyQt4 import QtGui, QtCore, Qt
from OkScroll import OkScrollBar
from PyQt4.QtCore import pyqtSlot
from OkListItem import OkTreeItem

class OkTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.selectedItem = None
        self.setHeaderHidden(True)
        #self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setSelectionMode(0)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMinimumWidth(250)
        self.setVerticalScrollBar(OkScrollBar())
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.itemEntered.connect(self.itemEnter)
        
    @pyqtSlot(str)        
    def search(self, text):
        if len(text) == 0:
            iterator = QtGui.QTreeWidgetItemIterator(self, QtGui.QTreeWidgetItemIterator.Hidden)
            while iterator.value() is not None:
                item = iterator.value()
                item.setHidden(False)
                iterator += 1
            self.collapseAll()
        else:
            iterator = QtGui.QTreeWidgetItemIterator(self)
            while iterator.value() is not None:
                item = iterator.value()
                step = 1
                if item.childCount() > 0 and text in item.text(0):
                    item.setHidden(False)
                    step += item.childCount()
                elif text not in item.text(0):
                    item.setHidden(True)
                elif item.childCount() == 0:
                    item.setHidden(False)
                    item.parent().setHidden(False)
                iterator += step
            self.expandAll()
        
class OkCaseTreeWidget(OkTreeWidget):
    def __init__(self, parent=None):
        OkTreeWidget.__init__(self, parent)
        self.setAcceptDrops(False)
        self.infoWidget = None
        self.editState = False
        self.setSortingEnabled(True)
        
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
            
    @pyqtSlot(OkTreeItem, int)    
    def itemEnter(self, item, col):
        if item != self.selectedItem:
            item.setBackgroundColor(col, QtGui.QColor(238,  238,  238))
        
    @pyqtSlot(OkTreeItem, int)
    def pressItem(self, item, col):
        if item.childCount() > 0:
            return
        self.topLevelWidget().basket.show()
        
        #itemdata = repr(item.data(Qt.Qt.UserRole))
        
        mimeData = QtCore.QMimeData()
        mimeData.setText(item.text(col))
        if item == self.selectedItem:
            id = item.data(col, Qt.Qt.UserRole)['id']
            top_level = self.indexOfTopLevelItem(item.parent())
            row = item.parent().indexOfChild(item)
            mimeData.setData('application/ok-case', '{"id":"%s","tl":"%d","row":"%d"}'%(id, top_level, row))
        
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
        
