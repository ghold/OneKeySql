from PyQt4 import QtGui, QtCore, Qt
class OkForwardWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        vlayout = QtGui.QHBoxLayout()
        verticalSpacer = QtGui.QSpacerItem(20, 30, 7, 0)
        vlayout.setDirection(QtGui.QBoxLayout.RightToLeft)        
        vlayout.addWidget(OkForwardButton("A"))
        vlayout.addSpacerItem(verticalSpacer)
        self.setLayout(vlayout)
        
class OkForwardButton(QtGui.QPushButton):
    def __init__(self, text, parent=None):
        QtGui.QPushButton.__init__(self, text, parent)
        self.setMaximumSize(30, 30)
        
    def mousePressEvent(self, event):
        print(1)
        event.accept()
        
    def paintEvent(self,  event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(33,  133,  197))
        tmpPainter.fillRect(QtCore.QRectF(self.rect().left(),  self.rect().top(),  self.rect().width(),
                self.rect().height()), tmpBrush)
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 14))
        tmpPainter.setPen(QtGui.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left(),  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()
