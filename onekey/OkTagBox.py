from PyQt4 import QtCore, Qt, Qt

class DragLabel(Qt.QLabel):
    def __init__(self, var, parent):
        Qt.QLabel.__init__(self, parent)
        self.var = var
        self.setText(self.var[1])
        self.setMinimumSize(7 * (len(self.text().encode('utf-8')) + len(self.text())), 30)
        self.setAlignment(Qt.Qt.AlignCenter)
        
        self.setAutoFillBackground(True)
        self.setFrameShape(Qt.QFrame.Panel)
        self.setFrameShadow(Qt.QFrame.Raised)
        
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
                
        tpl = r"标签类型：%s； 标签名称：%s； 默认值：%s； 可配置：%s"
        self.setToolTip(tpl%tuple(self.var))
        
    def mousePressEvent(self, event):
        hotSpot = event.pos()
        mimeData = QtCore.QMimeData()
        var = ','.join(self.var)
        mimeData.setText(var)
        mimeData.setData('application/x-point',
                '%d %d' % (self.pos().x(), self.pos().y()))

        pixmap = Qt.QPixmap(self.size())
        self.render(pixmap)

        drag = Qt.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()

class OkTagBox(Qt.QWidget):
    def __init__(self, tag, parent=None):
        Qt.QWidget.__init__(self, parent)
        x = 25
        y = 5
        for var in tag:
            var = self.makeupVar(var)
            wordLabel = DragLabel(var, self)
            if x >= (self.size().width() - wordLabel.minimumWidth()):
                x = 25
                y += 32
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.minimumWidth() + 2
        newPalette = self.palette()
        newPalette.setColor(Qt.QPalette.Window, Qt.QColor(50,  50,  50))
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
    
    def makeupVar(self, var):
        tp_var = var.copy()
        view = '否'
        if tp_var[3] is None:
            view = '是'
        if tp_var[2] is None:
            tp_var[2] = '无'
        tp_var[3] = view
        return tp_var
    
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
            pieces = mime.text().split(',')
            position = event.pos()
            point = QtCore.QPoint()

            pointxy = mime.data('application/x-point').split(' ')
            if len(pointxy) == 2:
               point.setX(pointxy[0].toInt()[0])
               point.setY(pointxy[1].toInt()[0])

            if pieces is not None:
                newLabel = DragLabel(pieces, self)
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
