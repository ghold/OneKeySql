from PyQt4 import QtGui, QtCore, Qt
import time

class OkListItem(QtGui.QListWidgetItem):
    def __init__(self, text, parent=None,  type=QtGui.QListWidgetItem.UserType):
        QtGui.QListWidgetItem.__init__(self, text, parent, type)
        
        #set background
        image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
        image.fill(QtGui.QColor(238,  238,  238))
        image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
        brush = QtGui.QBrush()
        brush.setTextureImage(image)
        self.setBackground(brush)
        
        self.setFlags(Qt.Qt.ItemIsUserCheckable|Qt.Qt.ItemIsEnabled|Qt.Qt.ItemIsDragEnabled)
        self.setFont(QtGui.QFont("微软雅黑", 12))
        self.setTextColor(QtGui.QColor(110,  110,  110))
        self.setSizeHint(QtCore.QSize(200, 41))
        self.state = False
    
    def setItemSelected(self, item):
        if self.listWidget().selectedItem is not None:
            self.listWidget().selectedItem.state = False
            tmpBrush = QtGui.QBrush(QtGui.QColor(238,  238,  238))
            self.listWidget().selectedItem.setBackground(tmpBrush)
            self.listWidget().selectedItem.setTextColor(QtGui.QColor(110,  110,  110))
        self.state = True
        self.listWidget().selectedItem = item

class OkAddonWidget(QtGui.QWidget):
    """
    work as a cover on OkListItem
    """
    def __init__(self, tooltip, parent=None):
        QtGui.QWidget.__init__(self)
        self.toolTip = OkToolTip(tooltip)
        self.parent =parent
        vlayout = QtGui.QHBoxLayout()
        verticalSpacer = QtGui.QSpacerItem(20, 30, 7, 0)
        vlayout.setDirection(QtGui.QBoxLayout.RightToLeft)        
        vlayout.addWidget(OkPutinButton())
        vlayout.addSpacerItem(verticalSpacer)
        self.setLayout(vlayout)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        if not self.parent.state:
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(77,  166,  234))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.parent.setBackground(brush)
            self.parent.setTextColor(QtGui.QColor(255,  255,  255))
            event.accept()
        
    def leaveEvent(self, event):
        if not self.parent.state:
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(238,  238,  238))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.parent.setBackground(brush)
            self.parent.setTextColor(QtGui.QColor(110,  110,  110))
            self.toolTip.hide()
            event.accept()
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton and not self.parent.state:
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(221, 221, 221))
            image.setPixel(0, 39, QtGui.qRgba(33, 133, 197, 255))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.parent.setBackground(brush)
            self.parent.setTextColor(QtGui.QColor(59,  66,  76))
            self.parent.setItemSelected(self.parent)
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.toolTip.isHidden():
            self.toolTip.setGeometry(event.globalX()+5, event.globalY()+5, 100, 200)
            #time.sleep(0.1)
            self.toolTip.show()
            event.accept()
        
class OkPencilButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setMaximumSize(18, 18)
        self.setFlat(1)
        self.setStyleSheet("QPushButton{"
                    "height: 18px;"
                    "width: 18px;"
                    "background: url(:/images/pencil_18x18_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/pencil_18x18_blue.png)"
                "}")
        
    def mousePressEvent(self, event):
        #self.parent().parent().parent().itemPressed.connect(self.parent().parent().parent().pressItem)
        event.accept()

class OkPutinButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
        self.setMaximumSize(24, 24)
        self.setFlat(1)
        self.setStyleSheet("QPushButton{"
                    "height: 18px;"
                    "width: 18px;"
                    "background: url(:/images/putin_24x24_gray.png)"
                "}"
                "QPushButton:hover {"
                    "background: url(:/images/pencil_18x18_blue.png)"
                "}")
        
    def mousePressEvent(self, event):
        self.topLevelWidget().showArgSetPad(self.parent().parent)
        event.accept()

class OkToolTip(QtGui.QTextEdit):
    def __init__(self, text, parent=None):
        QtGui.QTextEdit.__init__(self, text, parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        self.setSizePolicy(6, 6)
        
    def mouseMoveEvent(self, event):
        if self.isHidden():
            self.toolTip.setGeometry(event.globalX()+5, event.globalY()+5, 100, 200)
            #time.sleep(0.1)
            self.toolTip.show()
            event.accept()
