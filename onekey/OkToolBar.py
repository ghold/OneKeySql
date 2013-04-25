from PyQt4 import QtGui, QtCore, Qt

class OkMainToolBar(QtGui.QToolBar):
    
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)
            
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
                if self.parent().editWidget is not None:
                    self.parent().editWidget.update()
                self.update()
                event.accept()
            else:
                self.parent().showMaximized()
                if self.parent().editWidget is not None:
                    self.parent().editWidget.update()
                self.update()
                event.accept()
                
    def paintEvent(self,  event):
        self.setGeometryByHeight(30)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        #tmpBrush = QtGui.QBrush(QtGui.QColor(110,  202,  199))
        #tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()

class OkEditToolBar(QtGui.QToolBar):
    
    def __init__(self, parent=None):
        QtGui.QToolBar.__init__(self, parent)
            
    def setGeometryByHeight(self,  height):
        if self.parent() is not None:
            self.setGeometry(0,  0,  self.parent().rect().width(),  height)
            
    def mousePressEvent(self,event):
       if event.button() == QtCore.Qt.LeftButton:
           self.parent().parent().dragPosition = event.globalPos() - self.parent().parent().frameGeometry().topLeft()
           event.accept()
           
    def mouseMoveEvent(self,event):
        if event.buttons() ==QtCore.Qt.LeftButton and not self.parent().parent().isMaximized():
            self.parent().parent().move(event.globalPos() - self.parent().parent().dragPosition)
            event.accept() 
    
    def mouseDoubleClickEvent(self,  event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.parent().parent().isMaximized():
                self.parent().parent().showNormal()
                if self.parent().parent().editWidget is not None:
                    self.parent().parent().editWidget.update()
                self.update()
                self.parent().parent().update()
                event.accept()
            else:
                self.parent().parent().showMaximized()
                if self.parent().parent().editWidget is not None:
                    self.parent().parent().editWidget.update()
                self.update()
                self.parent().parent().update()
                event.accept()
                
    def paintEvent(self,  event):
        self.setGeometryByHeight(30)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        #tmpBrush = QtGui.QBrush(QtGui.QColor(11,  202,  199))
        #tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.end()
        event.accept()
