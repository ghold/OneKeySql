from PyQt4 import QtGui, QtCore, Qt
from OkModel import OkModel
from OkXmlHandler import OkTestcaseHandler
from OkListItem import OkListItem

class OkListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setSelectionMode(0)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setAcceptDrops(True)
        
    def makeupCase(self, file):
        self.data = OkModel(file, OkTestcaseHandler, self)
        self.testcase_count = self.data.item(0).rowCount()
        for index in range(self.testcase_count):
            ok_list_item = OkListItem( self.data.item(0).child(index).text(), self)
            self.addItem(ok_list_item)
