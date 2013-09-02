from PyQt4 import QtGui, QtCore, Qt

class OkTreeItem(QtGui.QTreeWidgetItem):
    def __init__(self, text, parent=None,  type=QtGui.QTreeWidgetItem.Type):
        QtGui.QTreeWidgetItem.__init__(self, parent, type)
        self.setText(0, text)
        self.state = False
        
    def setItemSelected(self, item):
        if self.treeWidget().selectedItem is not None:
            self.treeWidget().selectedItem.state = False
        self.state = True
        self.treeWidget().selectedItem = item
