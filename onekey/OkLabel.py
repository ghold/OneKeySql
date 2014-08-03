from PyQt4 import Qt, QtCore, Qt

class OkEditWidgetLabel(Qt.QLabel):
    def __init__(self, text, parent=None, flags=Qt.Qt.Widget):
        Qt.QLabel.__init__(self, text, parent, flags)
        
    def paintEvent(self, event):
        self.setMinimumSize(200, 40)
        tmpPainter = Qt.QPainter()
        tmpPainter.begin(self)
        #tmpBrush = Qt.QBrush(Qt.QColor(33,  133,  197))
        #tmpPainter.fillRect(QtCore.QRectF(self.rect().left() + 36,  self.rect().top(),  self.rect().width(),
        #        self.rect().height()), tmpBrush)
        #tmpPainter.drawImage(QtCore.QPoint(0, 0), self.image.scaled(35, 35))
        tmpPainter.setFont(Qt.QFont("微软雅黑", 14))
        tmpPainter.setPen(Qt.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignVCenter, self.text())
        tmpPainter.end()
        event.accept()

class OkTagLabel(Qt.QLabel):
    def __init__(self, text, parent=None, flags=Qt.Qt.Widget):
        Qt.QLabel.__init__(self, text, parent, flags)
        self.setStyleSheet("QLabel{"
                    "height: 25px;"
                    "font-family: '微软雅黑';"
                    "color: #FFFFFF;"
                    "font-size: 15px;"
                    "padding-left: 20px"
                "}")
