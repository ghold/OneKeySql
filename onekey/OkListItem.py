from PyQt4 import QtGui, QtCore, Qt

class OkListItem(QtGui.QListWidgetItem):
    def __init__(self, text,  parent=None,  type=QtGui.QListWidgetItem.UserType):
        QtGui.QListWidgetItem.__init__(self, text,  parent, type)
        tmpBrush = QtGui.QBrush(QtGui.QColor(226,  226,  226))
        self.setBackground(tmpBrush)
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setWhatsThis("hello")
        self.setSizeHint(QtCore.QSize(200, 40))
        