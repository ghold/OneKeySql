from PyQt4 import QtGui, Qt

class OkCaseListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        QtGui.QListWidget.__init__(self, parent)
        self.setFrameStyle(QtGui.QFrame.NoFrame)
        self.setSelectionMode(0)
        self.setFocusPolicy(Qt.Qt.NoFocus)
        self.setAcceptDrops(True)
            

