from PyQt4 import QtGui, QtCore, Qt

class OkListItem(QtGui.QListWidgetItem):
    def __init__(self, text,  parent=None,  type=QtGui.QListWidgetItem.UserType):
        QtGui.QListWidgetItem.__init__(self, text,  parent, type)
        #tmpBrush = QtGui.QBrush(QtGui.QColor(226,  226,  226))
        tmpBrush = QtGui.QBrush()
        tmpBrush.setTextureImage(QtGui.QImage(":/images/itembg_1x40.png"))
        self.setBackground(tmpBrush)
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setWhatsThis("hello")
        self.setFont(QtGui.QFont("微软雅黑", 12))
        self.setTextColor(QtGui.QColor(59,  66,  76))
        self.setSizeHint(QtCore.QSize(200, 40))
