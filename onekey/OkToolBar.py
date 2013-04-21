from PyQt4 import QtGui, QtCore, Qt

class OkToolBar(QtGui.QToolBar):
    
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)
        self.setGeometryByHeight(30)
            
    def setGeometryByHeight(self,  height):
        if self.parent() is not None:
            self.setGeometry(0,  0,  self.parent().rect().width(),  height)
            
    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.parent().dragPosition = event.globalPos() - self.parent().frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.parent().isMaximized():
            self.parent().move(event.globalPos() - self.parent().dragPosition)
            event.accept() 
    
    def mouseDoubleClickEvent(self,  event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.parent().isMaximized():
                self.parent().showNormal()
                self.setGeometryByHeight(30)
                event.accept()
            else:
                self.parent().showMaximized()
                self.setGeometryByHeight(30)
                event.accept()
                
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(110,  202,  199))
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()
