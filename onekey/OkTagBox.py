from PyQt4 import QtCore, QtGui, Qt

class DragLabel(QtGui.QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(text, parent)
        self.setMinimumSize(4 * (len(self.text().encode('utf-8')) + len(self.text())), 30)
        self.setAlignment(Qt.Qt.AlignCenter)
        
        self.setAutoFillBackground(True)
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        
        self.setStyleSheet("QLabel{"
                    "border:1px solid #000000;"
                    "background-color: #FF7F66;"
                    "height: 25px;"
                     "font-family: '微软雅黑';"
                    "color: #FFFFFF;"
                    "font-size: 14px;"
                "}"
                "QLabel:hover{"
                    "border:1px solid #9BBAAC;"
                "}"
                "QLabel:focus{"
                    "border:1px solid #7ECEFD;"              
                "}")
    
    def mousePressEvent(self, event):
        hotSpot = event.pos()
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        mimeData.setData('application/x-point',
                '%d %d' % (self.pos().x(), self.pos().y()))

        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()

class OkTagBox(QtGui.QWidget):
    def __init__(self, tag, parent=None):
        QtGui.QWidget.__init__(self, parent)
        x = 25
        y = 5
        for word in tag:
            wordLabel = DragLabel(word, self)
            if x >= (self.size().width() - wordLabel.minimumWidth()):
                x = 25
                y += 32
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.minimumWidth() + 2            
        newPalette = self.palette()
        newPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(50,  50,  50))
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
    
    def resizeEvent(self, event):
        x = 25
        y = 5
        for wordLabel in self.children():
            if x >= (event.size().width() - wordLabel.minimumWidth()):
                x = 25
                y += 32
            wordLabel.move(x, y)
            x += wordLabel.minimumWidth() + 2
        self.setMinimumHeight(y+40)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            mime = event.mimeData()
            pieces = mime.text().split()
            position = event.pos()
            point = QtCore.QPoint()

            pointxy = mime.data('application/x-point').split(' ')
            if len(pointxy) == 2:
               point.setX(pointxy[0].toInt()[0])
               point.setY(pointxy[1].toInt()[0])

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(point)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()
