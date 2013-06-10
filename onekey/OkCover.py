from PyQt4 import QtGui, QtCore, Qt

class OkCover(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(0, 0, 200,  self.parent().height()))
        #palette
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(255,255,255,128))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(0, 0, 200 ,  self.parent().height()))
        
