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
        
class OkExecButton(QtGui.QPushButton):
    def __init__(self,  text, parent=None):
        QtGui.QPushButton.__init__(self, text, parent)
        
        self.setStyleSheet("QPushButton{"
                    "border:1px solid #000000;"
                    "background-color: #656565;"
                    "height: 25px;"
                    "font-size: 16px;"
                    "font-family: '微软雅黑';"
                    "padding-left:3px;"
                    "width:300px;"
                    "color: #FFF"
                "}"
                "QPushButton:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QPushButton:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
        
