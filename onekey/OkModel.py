from PyQt4 import QtGui, QtCore, Qt
from OkListItem import OkListItem
from xml.sax import parse
from OkScrollBar import OkScrollBar
from PyQt4.QtCore import pyqtSlot

class OkListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        #self.setSelectionMode(0)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setMinimumWidth(250)
        self.setVerticalScrollBar(OkScrollBar())
        self.setSpacing(1)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
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
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        
    def startDrag(self, supportedActions):
        
        item = self.currentItem()
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
        
        
class OkModel(object):
    data = []
    
    def __init__(self,  file, handler, parent = None):
        self.handler = handler()
        parse(file, self.handler)
        self.data = self.handler.getXmlData()
        
    def makeupTestList(self):
        self.test_list = OkListWidget()
        for key,  val in self.data.items():
            #print(key)
            item = OkListItem(key, self.test_list)
            item.setData(Qt.Qt.UserRole, val)
            self.test_list.addItem(item)
        return self.test_list
            
    def makeupStepList(self, item):
        self.step_list = OkListWidget()
        tmp_data = item.data(Qt.Qt.UserRole)
        step_count = len(tmp_data["data"]["steps"])
        #print(1)
        for i in range(step_count):
            val = tmp_data["data"]["steps"][i]
            item = OkListItem("_".join((val["from"], val["type"], val["data_id"])), self.step_list)
            #print(item.text())
            item.setData(Qt.Qt.UserRole, val)
            self.step_list.addItem(item)
        return self.step_list
