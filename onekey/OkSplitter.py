from PyQt4 import QtGui, QtCore, Qt

class OkSplitter(QtGui.QSplitter):
    def __init__(self, parent=None):
        QtGui.QSplitter.__init__(self, parent)
        self.setHandleWidth(1)
        self.setChildrenCollapsible(False)
        
        self.setStyleSheet("QSplitter::handle{"
                    "border: 0px;"
                    "color: #fff;"
                "}"
                "QSplitter{"
                    "border: 0px;"
                    "background-color: #fff;"
                "}")
