from PyQt4 import QtGui, QtCore, Qt

class OkTreeWidget(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        QtGui.QTreeWidget.__init__(self, parent)
        self.setHeaderHidden(True)
        
class OkCaseTreeWidget(OkTreeWidget):
    def __init__(self, parent=None):
        OkTreeWidget.__init__(self, parent)
        self.setAcceptDrops(False)
        self.infoWidget = None
        self.editState = False
        self.setSortingEnabled(True)
