from PyQt4 import QtGui, QtCore, Qt

class OkModuleButton(QtGui.QPushButton):
    def __init__(self,  text, image, parent=None):
        QtGui.QPushButton.__init__(self, text, parent)
        self.setMinimumSize(200, 35)
        self.image = image
        
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left() + 36,  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.drawImage(QtCore.QPoint(0, 0), self.image.scaled(35, 35))
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 14))
        tmpPainter.setPen(QtGui.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() + 50,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()
