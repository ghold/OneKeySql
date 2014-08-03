from PyQt4 import Qt, QtCore

class OkCover(Qt.QWidget):
    def __init__(self, parent=None):
        Qt.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setGeometry(QtCore.QRect(0, 0, 200,  self.parent().height()))
        #palette
        palette = Qt.QPalette()
        palette.setColor(Qt.QPalette.Background, Qt.QColor(255,255,255,128))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
    def paintEvent(self, event):
        self.setGeometry(QtCore.QRect(0, 0, 200 ,  self.parent().height()))
        
