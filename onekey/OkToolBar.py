from PyQt4 import QtGui, QtCore, Qt

class OkToolBar(QtGui.QToolBar):
    
    def __init__(self,  text, parent=None):
        QtGui.QToolBar.__init__(self, parent)
        
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(110,  202,  199))
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()
