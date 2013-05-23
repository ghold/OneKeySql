from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import pyqtSlot

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
    def __init__(self, tooltip, item, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #self.toolTip = OkToolTip(tooltip)
        self.setToolTip(tooltip)
        self.item =item
        vlayout = QtGui.QHBoxLayout()
        verticalSpacer = QtGui.QSpacerItem(20, 30, 7, 0)
        vlayout.setDirection(QtGui.QBoxLayout.RightToLeft)        
        vlayout.addWidget(OkPutinButton())
        vlayout.addSpacerItem(verticalSpacer)
        self.setLayout(vlayout)
        self.setMouseTracking(True)
        
    def enterEvent(self, event):
        if not self.item.state:
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(77,  166,  234))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(brush)
            self.item.setTextColor(QtGui.QColor(255,  255,  255))
            
            #point = self.mapTo(self.topLevelWidget(), self.geometry().topLeft())
            #self.toolTip.setParent(self.topLevelWidget())
            #self.toolTip.setGeometry(point.x() - 10, (point.y() + 42 - 2*10)/2,
                    #self.geometry().width() + 20, self.geometry().height() + 20)
            #self.toolTip.show()
            event.accept()
        
    def leaveEvent(self, event):
        if not self.item.state:
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(238,  238,  238))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(brush)
            self.item.setTextColor(QtGui.QColor(110,  110,  110))
            event.accept()
    
    def mousePressEvent(self, event):
        if event.buttons() == Qt.Qt.LeftButton and not self.item.state:
            #change background
            image = QtGui.QImage(1, 41, QtGui.QImage.Format_RGB32)
            image.fill(QtGui.QColor(221, 221, 221))
            image.setPixel(0, 39, QtGui.qRgba(33, 133, 197, 255))
            image.setPixel(0, 40, QtGui.qRgba(255, 255, 255, 255))
            brush = QtGui.QBrush()
            brush.setTextureImage(image)
            self.item.setBackground(brush)
            self.item.setTextColor(QtGui.QColor(59,  66,  76))
            self.item.setItemSelected(self.item)
            #show info
            infoWidget = self.item.listWidget().infoWidget
            infoWidget.infoGeneratorUTF8(self.item)
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
        self.topLevelWidget().showArgSetPad(self.parent().item)
        event.accept()
##disable
class OkToolTip(QtGui.QTextEdit):
    def __init__(self, text, parent=None):
        QtGui.QTextEdit.__init__(self, text, parent)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)
        self.setStyleSheet("QTextEdit{"
                    "border: 0px;"
                    "background: #656565"
                "}")
        self.setSizePolicy(6, 6)
        
    def leaveEvent(self, event):
        self.hide()
        event.accept()
