from PyQt4 import QtGui, QtCore, Qt

class OkModuleButton(QtGui.QPushButton):
    def __init__(self,  text, parent=None):
        QtGui.QPushButton.__init__(self, text, parent)
        self.setMinimumSize(200, 35)
        
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(110,  202,  199))
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 16))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() + 10,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()
