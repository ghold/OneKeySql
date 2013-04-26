from PyQt4 import QtCore, QtGui, Qt

class OkTextEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        QtGui.QTextEdit.__init__(self, parent)
        tmpPalette = QtGui.QPalette()
        tmpPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(62,  69,  76))
        self.setPalette(tmpPalette)
        
