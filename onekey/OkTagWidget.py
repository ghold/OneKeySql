from PyQt4 import QtCore, QtGui, Qt

class DragLabel(QtGui.QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(text, parent)
        self.setMinimumSize(7 * (len(self.text().encode('utf-8')) + len(self.text())), 30)
        
        self.setAutoFillBackground(True)
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        
    def paintEvent(self, event):
        tmpPainter = QtGui.QPainter()
        tmpPainter.begin(self)
        tmpBrush = QtGui.QBrush(QtGui.QColor(255, 127, 107))
        tmpPainter.fillRect(QtCore.QRectF(self.rect()), tmpBrush)
        tmpPainter.setFont(QtGui.QFont("微软雅黑", 14))
        tmpPainter.setPen(QtGui.QColor(255,  255,  255))
        tmpPainter.drawText(QtCore.QRectF(self.rect().left() ,  self.rect().top(),  self.rect().width(),
                self.rect().height()),  Qt.Qt.AlignCenter, self.text())
        tmpPainter.end()
        event.accept()

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


class OkTagWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OkTagWidget, self).__init__(parent)

        x = 5
        y = 5

        for word in "我的 熱門呢 誒反對 sdf sdf sdf sdfsdf sdfsd dfsf sdf sdf sdf sdfsdf sdfsd dfsf sdf sdf sdf sdf我的 熱門呢 誒反對 sdf sdf sdf sdfsdf sdfsd dfsf sdf sdf sdf sdfsdf sdfsd dfsf sdf sdf sdf sdf".split():
            wordLabel = DragLabel(word, self)
            if x >= (400 - wordLabel.minimumWidth()):
                x = 5
                y += 32
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.minimumWidth() + 2
            

        newPalette = self.palette()
        newPalette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, y+40)

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


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec_())
