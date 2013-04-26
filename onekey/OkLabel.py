from PyQt4 import QtGui, QtCore, Qt

class OkEditWidgetLabel(QtGui.QLabel):
    def __init__(self, text, parent=None, flags=Qt.Qt.Widget):
        QtGui.QLabel.__init__(self, text, parent, flags)
        
    def paintEvent(self, event):
        self.setMinimumSize(200, 40)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() + 36,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        #tmpPainter.drawImage(QtCore.QPoint(0, 0), self.image.scaled(35, 35))
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 14))
        tmpPainter.setPen(QtGui.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()

class OkTagLabel(QtGui.QLabel):
    def __init__(self, text, parent=None, flags=Qt.Qt.Widget):
        QtGui.QLabel.__init__(self, text, parent, flags)
        
    def paintEvent(self, event):
        self.setMinimumSize(30, 20)
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        #tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
        #tmpPainter.fillRect(QtCore.QRectF(self.rect().left() + 36,  self.rect().top(),  self.rect().width(),
         #       self.rect().height()), tmpBrush)
        #tmpPainter.drawImage(QtCore.QPoint(0, 0), self.image.scaled(35, 35))
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 10))
        tmpPainter.setPen(QtGui.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()
