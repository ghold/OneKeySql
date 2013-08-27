from PyQt4 import QtGui, QtCore, Qt

class OkTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.setText(0, "hello")
        
        
